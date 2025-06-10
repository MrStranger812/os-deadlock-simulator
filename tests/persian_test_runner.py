#!/usr/bin/env python3
"""
اجرای تست‌های آموزشی شبیه‌ساز بن‌بست - نسخه اصلاح شده برای مشکلات فونت

Fixed Persian Educational Test Runner - Font Issues Resolved

This version includes proper font handling for Linux systems and improved error handling.
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime
import json
import warnings
from typing import List, Dict, Any

# Suppress matplotlib font warnings during startup
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib.font_manager')

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Configure matplotlib before importing visualization components
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend to prevent display issues

from tests.test_scenarios import (
    create_simple_deadlock,
    create_dining_philosophers,
    create_resource_allocation_scenario,
    create_no_deadlock_scenario,
    create_chain_deadlock,
    save_system_state,
    restore_system_state
)
from src.detection import DeadlockDetector
from src.resolution import DeadlockResolver

# Import the fixed visualizer
try:
    from src.visualization.educational_visualizer import EducationalVisualizer
    VISUALIZER_AVAILABLE = True
    print("✅ Educational visualizer loaded successfully")
except ImportError as e:
    print(f"⚠️ Visualizer import failed: {e}")
    VISUALIZER_AVAILABLE = False

class PersianEducationalTestRunner:
    """
    اجرای تست جامع با حل مشکلات فونت و بهبود مدیریت خطا
    
    Comprehensive test runner with font issues resolved and improved error handling.
    """
    
    def __init__(self, base_output_dir: str = "educational_results", language: str = "persian"):
        """Initialize the test runner with proper error handling."""
        self.base_output_dir = Path(base_output_dir)
        self.language = language
        self.project_dir = None
        
        # Setup logging to reduce font warnings
        import logging
        logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)
        
        # Persian translations for scenarios
        self.persian_scenarios = {
            'simple_deadlock': {
                'name': 'بن‌بست ساده دو فرآیندی',
                'function': create_simple_deadlock,
                'description': 'سناریوی کلاسیک بن‌بست دایره‌ای دو فرآیند',
                'learning_objectives': [
                    'درک تشکیل بن‌بست پایه',
                    'شناسایی شرط انتظار دایره‌ای',
                    'تشخیص چرخه‌های نمودار تخصیص منابع'
                ]
            },
            'dining_philosophers_3': {
                'name': 'فیلسوفان غذاخور (۳ فیلسوف)',
                'function': lambda: create_dining_philosophers(3),
                'description': 'مسئله فیلسوفان غذاخور در مقیاس کوچک',
                'learning_objectives': [
                    'درک تضادهای اشتراک منابع',
                    'مشاهده بن‌بست چندین فرآیند',
                    'یادگیری الگوهای بن‌بست متقارن'
                ]
            },
            'dining_philosophers_5': {
                'name': 'فیلسوفان غذاخور (۵ فیلسوف)',
                'function': lambda: create_dining_philosophers(5),
                'description': 'سناریوی کلاسیک بن‌بست فیلسوفان غذاخور',
                'learning_objectives': [
                    'تحلیل رقابت منابع در مقیاس بزرگ‌تر',
                    'درک مقیاس‌پذیری مسائل بن‌بست',
                    'مقایسه با گروه‌های کوچک‌تر فیلسوفان'
                ]
            },
            'dining_philosophers_7': {
                'name': 'فیلسوفان غذاخور (۷ فیلسوف)',
                'function': lambda: create_dining_philosophers(7),
                'description': 'سناریوی بزرگ فیلسوفان غذاخور',
                'learning_objectives': [
                    'مشاهده الگوهای پیچیده بن‌بست',
                    'درک رشد پیچیدگی تشخیص',
                    'تحلیل افزایش دشواری حل'
                ]
            },
            'complex_allocation': {
                'name': 'تخصیص پیچیده چند منبعه',
                'function': create_resource_allocation_scenario,
                'description': 'چندین فرآیند در رقابت برای انواع مختلف منابع',
                'learning_objectives': [
                    'درک بن‌بست‌های چند منبعه',
                    'یادگیری ماتریس‌های تخصیص پیچیده',
                    'تحلیل کاربرد الگوریتم بانکدار'
                ]
            },
            'no_deadlock': {
                'name': 'حالت امن سیستم (بدون بن‌بست)',
                'function': create_no_deadlock_scenario,
                'description': 'سیستم با درخواست‌های منابع اما بدون بن‌بست',
                'learning_objectives': [
                    'تمایز بین بن‌بست و انتظار',
                    'درک حالات امن در مقابل ناامن',
                    'یادگیری تشخیص مثبت کاذب'
                ]
            },
            'chain_deadlock': {
                'name': 'الگوی بن‌بست زنجیره‌ای',
                'function': create_chain_deadlock,
                'description': 'زنجیره دایره‌ای وابستگی‌ها میان فرآیندها',
                'learning_objectives': [
                    'شناسایی الگوهای بن‌بست زنجیره‌ای',
                    'درک انتقال‌پذیری در وابستگی‌های منابع',
                    'تحلیل تشخیص در زنجیره‌های خطی در مقابل دایره‌ای'
                ]
            }
        }
        
        # English scenarios as fallback
        self.english_scenarios = {
            'simple_deadlock': {
                'name': 'Simple Two-Process Deadlock',
                'function': create_simple_deadlock,
                'description': 'Classic two-process circular deadlock scenario',
                'learning_objectives': [
                    'Understand basic deadlock formation',
                    'Identify circular wait condition',
                    'Recognize resource allocation graph cycles'
                ]
            },
            'dining_philosophers_3': {
                'name': 'Dining Philosophers (3 Philosophers)',
                'function': lambda: create_dining_philosophers(3),
                'description': 'Small-scale dining philosophers problem',
                'learning_objectives': [
                    'Understand resource sharing conflicts',
                    'See how multiple processes can deadlock',
                    'Learn about symmetric deadlock patterns'
                ]
            },
            'dining_philosophers_5': {
                'name': 'Dining Philosophers (5 Philosophers)',
                'function': lambda: create_dining_philosophers(5),
                'description': 'Classic dining philosophers deadlock scenario',
                'learning_objectives': [
                    'Analyze larger-scale resource contention',
                    'Understand scalability of deadlock problems',
                    'Compare with smaller philosopher groups'
                ]
            },
            'dining_philosophers_7': {
                'name': 'Dining Philosophers (7 Philosophers)',
                'function': lambda: create_dining_philosophers(7),
                'description': 'Large dining philosophers scenario',
                'learning_objectives': [
                    'Observe complex deadlock patterns',
                    'Understand detection complexity growth',
                    'Analyze resolution difficulty scaling'
                ]
            },
            'complex_allocation': {
                'name': 'Complex Multi-Resource Allocation',
                'function': create_resource_allocation_scenario,
                'description': 'Multiple processes competing for various resource types',
                'learning_objectives': [
                    'Understand multi-resource deadlocks',
                    'Learn about complex allocation matrices',
                    'Analyze banker\'s algorithm application'
                ]
            },
            'no_deadlock': {
                'name': 'Safe System State (No Deadlock)',
                'function': create_no_deadlock_scenario,
                'description': 'System with resource requests but no deadlock',
                'learning_objectives': [
                    'Distinguish between deadlock and waiting',
                    'Understand safe vs unsafe states',
                    'Learn about false positive detection'
                ]
            },
            'chain_deadlock': {
                'name': 'Chain Deadlock Pattern',
                'function': create_chain_deadlock,
                'description': 'Circular chain of dependencies among processes',
                'learning_objectives': [
                    'Identify chain-like deadlock patterns',
                    'Understand transitivity in resource dependencies',
                    'Analyze detection in linear vs circular chains'
                ]
            }
        }
        
        self.scenarios = self.persian_scenarios if language == 'persian' else self.english_scenarios
    
    def run_all_scenarios(self, selected_scenarios: List[str] = None) -> Dict[str, Any]:
        """Run all scenarios with improved error handling and font management."""
        
        # Create project directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.project_dir = self.base_output_dir / f"simulation_project_{timestamp}"
        self.project_dir.mkdir(parents=True, exist_ok=True)
        
        if self.language == 'persian':
            print(f"🎓 شروع پروژه آموزشی شبیه‌سازی بن‌بست")
            print(f"📁 پوشه خروجی: {self.project_dir}")
            if not VISUALIZER_AVAILABLE:
                print("⚠️ تصویرسازی غیرفعال - فقط فایل‌های متنی تولید می‌شوند")
        else:
            print(f"🎓 Starting Educational Deadlock Simulation Project")
            print(f"📁 Output directory: {self.project_dir}")
            if not VISUALIZER_AVAILABLE:
                print("⚠️ Visualization disabled - only text files will be generated")
        print("=" * 70)
        
        # Determine which scenarios to run
        scenarios_to_run = selected_scenarios or list(self.scenarios.keys())
        
        # Results tracking
        project_results = {
            'timestamp': timestamp,
            'language': self.language,
            'project_directory': str(self.project_dir),
            'scenarios_run': [],
            'summary_statistics': {},
            'generated_files': [],
            'visualizer_available': VISUALIZER_AVAILABLE
        }
        
        # Run each scenario
        for scenario_id in scenarios_to_run:
            if scenario_id not in self.scenarios:
                print(f"⚠️ Unknown scenario: {scenario_id}")
                continue
                
            scenario_info = self.scenarios[scenario_id]
            if self.language == 'persian':
                print(f"\n🔬 اجرای سناریو: {scenario_info['name']}")
                print(f"📖 توضیح: {scenario_info['description']}")
            else:
                print(f"\n🔬 Running Scenario: {scenario_info['name']}")
                print(f"📖 Description: {scenario_info['description']}")
            print("-" * 50)
            
            try:
                scenario_result = self._run_single_scenario(scenario_id, scenario_info)
                project_results['scenarios_run'].append(scenario_result)
                project_results['generated_files'].extend(scenario_result['generated_files'])
                
                if self.language == 'persian':
                    print(f"✅ تکمیل شد: {scenario_info['name']}")
                else:
                    print(f"✅ Completed: {scenario_info['name']}")
                
            except Exception as e:
                if self.language == 'persian':
                    print(f"❌ ناموفق: {scenario_info['name']} - {str(e)}")
                else:
                    print(f"❌ Failed: {scenario_info['name']} - {str(e)}")
                project_results['scenarios_run'].append({
                    'scenario_id': scenario_id,
                    'name': scenario_info['name'],
                    'status': 'failed',
                    'error': str(e)
                })
        
        # Generate project summary
        if self.language == 'persian':
            print(f"\n📊 تولید خلاصه پروژه...")
        else:
            print(f"\n📊 Generating Project Summary...")
        self._generate_project_summary(project_results)
        
        # Create index file
        self._create_project_index(project_results)
        
        if self.language == 'persian':
            print(f"\n🎉 پروژه آموزشی تکمیل شد!")
            print(f"📁 همه مطالب در پوشه ذخیره شد: {self.project_dir}")
            print(f"📄 فایل {self.project_dir}/index.html را برای مشاهده نتایج باز کنید")
        else:
            print(f"\n🎉 Educational project completed!")
            print(f"📁 All materials saved to: {self.project_dir}")
            print(f"📄 Open {self.project_dir}/index.html to view complete results")
        
        return project_results
    
    def _run_single_scenario(self, scenario_id: str, scenario_info: Dict) -> Dict[str, Any]:
        """Run a single scenario with improved error handling."""
        
        # Create scenario directory
        scenario_dir = self.project_dir / scenario_id
        scenario_dir.mkdir(exist_ok=True)
        
        # Initialize system
        if self.language == 'persian':
            print("🔧 ساخت سیستم...")
        else:
            print("🔧 Creating system...")
        self.system = scenario_info['function']()  # Store system as instance variable
        
        generated_files = []
        
        # Run deadlock detection
        if self.language == 'persian':
            print("🔍 اجرای تشخیص بن‌بست...")
        else:
            print("🔍 Running deadlock detection...")
        detector = DeadlockDetector(self.system)
        rag_deadlocked, rag_processes = detector.detect_using_resource_allocation_graph()
        banker_deadlocked, banker_processes = detector.detect_using_bankers_algorithm()
        
        # Test resolution if deadlock detected
        resolution_results = {}
        if rag_deadlocked:
            if self.language == 'persian':
                print("🛠️ آزمایش راهبردهای حل...")
            else:
                print("🛠️ Testing resolution strategies...")
            resolver = DeadlockResolver(self.system, detector)
            original_state = save_system_state(self.system)
            
            # Test each resolution strategy
            for strategy in ['termination', 'preemption', 'rollback']:
                restore_system_state(self.system, original_state)
                
                try:
                    if strategy == 'termination':
                        success = resolver._resolve_by_termination(rag_processes.copy(), priority_based=False)
                    elif strategy == 'preemption':
                        success = resolver._resolve_by_preemption(rag_processes.copy(), priority_based=False)
                    else:  # rollback
                        success = resolver._resolve_by_rollback(rag_processes.copy(), priority_based=False)
                    
                    resolution_results[strategy] = success
                    
                except Exception as e:
                    resolution_results[strategy] = False
                    if self.language == 'persian':
                        print(f"⚠️ راهبرد حل {strategy} ناموفق: {e}")
                    else:
                        print(f"⚠️ Resolution strategy {strategy} failed: {e}")
            
            # Restore original state for visualization
            restore_system_state(self.system, original_state)
        
        # Generate educational materials
        if self.language == 'persian':
            print("🎨 ساخت مطالب آموزشی...")
        else:
            print("🎨 Creating educational materials...")
        
        # Try to create visualizations if available
        if VISUALIZER_AVAILABLE:
            try:
                visualizer = EducationalVisualizer(self.system, language=self.language)
                viz_files = visualizer.create_comprehensive_visualization(
                    deadlocked_processes=rag_processes if rag_deadlocked else None,
                    output_dir=str(scenario_dir),
                    scenario_name=scenario_id
                )
                generated_files.extend(list(viz_files.values()))
            except Exception as e:
                if self.language == 'persian':
                    print(f"⚠️ خطا در تصویرسازی: {e}")
                    print("📝 ادامه با تولید فایل‌های متنی...")
                else:
                    print(f"⚠️ Visualization error: {e}")
                    print("📝 Continuing with text file generation...")
        
        # Always create text-based educational content
        self._create_scenario_comparison_chart(scenario_dir, rag_deadlocked, banker_deadlocked, 
                                             rag_processes, banker_processes)
        generated_files.append(str(scenario_dir / "algorithm_comparison.txt"))
        
        if resolution_results:
            self._create_resolution_summary(scenario_dir, resolution_results)
            generated_files.append(str(scenario_dir / "resolution_analysis.txt"))
        
        self._create_learning_guide(scenario_dir, scenario_info, rag_deadlocked, rag_processes)
        generated_files.append(str(scenario_dir / "learning_guide.txt"))
        
        # Create simple system state summary
        self._create_system_state_text(scenario_dir, rag_deadlocked, rag_processes)
        generated_files.append(str(scenario_dir / "system_state_summary.txt"))
        
        # Prepare result summary
        result = {
            'scenario_id': scenario_id,
            'name': scenario_info['name'],
            'status': 'completed',
            'deadlock_detected': rag_deadlocked,
            'deadlocked_processes': rag_processes,
            'detection_results': {
                'rag': {'deadlocked': rag_deadlocked, 'processes': rag_processes},
                'banker': {'deadlocked': banker_deadlocked, 'processes': banker_processes}
            },
            'resolution_results': resolution_results,
            'generated_files': [
                str(Path(path).relative_to(self.project_dir)) for path in generated_files
            ],
            'scenario_directory': str(scenario_dir.relative_to(self.project_dir))
        }
        
        return result
    
    def _create_system_state_text(self, scenario_dir: Path, deadlock_detected: bool, deadlocked_processes: List[int]):
        """Create a text-based system state summary."""
        
        if self.language == 'persian':
            summary = f"""
خلاصه وضعیت سیستم
================

زمان سیستم: {self.system.time}
وضعیت بن‌بست: {'🔴 شناسایی شد' if deadlock_detected else '🟢 شناسایی نشد'}
"""
            if deadlock_detected:
                summary += f"فرآیندهای آسیب‌دیده: {', '.join([f'P{pid}' for pid in deadlocked_processes])}\n"
            
            summary += f"""

جزئیات فرآیندها:
===============
"""
            for pid, process in self.system.processes.items():
                status_persian = {
                    'RUNNING': 'در حال اجرا',
                    'WAITING': 'در انتظار',
                    'TERMINATED': 'پایان یافته'
                }
                summary += f"فرآیند P{pid}: {status_persian.get(process.status, process.status)}\n"
                if process.resources_held:
                    held = [f"R{r.rid}" for r in process.resources_held]
                    summary += f"  - منابع نگهداری‌شده: {', '.join(held)}\n"
                if process.resources_requested:
                    requested = [f"R{r.rid}" for r in process.resources_requested]
                    summary += f"  - منابع درخواستی: {', '.join(requested)}\n"
                summary += "\n"
            
            summary += f"""
جزئیات منابع:
===========
"""
            for rid, resource in self.system.resources.items():
                summary += f"منبع R{rid}: {resource.available_instances}/{resource.total_instances} موجود\n"
                if resource.allocated_to:
                    allocated = [f"P{pid}({count})" for pid, count in resource.allocated_to.items()]
                    summary += f"  - تخصیص یافته به: {', '.join(allocated)}\n"
                summary += "\n"
                
        else:
            summary = f"""
SYSTEM STATE SUMMARY
==================

System Time: {self.system.time}
Deadlock Status: {'🔴 DETECTED' if deadlock_detected else '🟢 NOT DETECTED'}
"""
            if deadlock_detected:
                summary += f"Affected Processes: {', '.join([f'P{pid}' for pid in deadlocked_processes])}\n"
            
            summary += f"""

Process Details:
==============
"""
            for pid, process in self.system.processes.items():
                summary += f"Process P{pid}: {process.status}\n"
                if process.resources_held:
                    held = [f"R{r.rid}" for r in process.resources_held]
                    summary += f"  - Holding: {', '.join(held)}\n"
                if process.resources_requested:
                    requested = [f"R{r.rid}" for r in process.resources_requested]
                    summary += f"  - Requesting: {', '.join(requested)}\n"
                summary += "\n"
            
            summary += f"""
Resource Details:
===============
"""
            for rid, resource in self.system.resources.items():
                summary += f"Resource R{rid}: {resource.available_instances}/{resource.total_instances} available\n"
                if resource.allocated_to:
                    allocated = [f"P{pid}({count})" for pid, count in resource.allocated_to.items()]
                    summary += f"  - Allocated to: {', '.join(allocated)}\n"
                summary += "\n"
        
        with open(scenario_dir / "system_state_summary.txt", 'w', encoding='utf-8') as f:
            f.write(summary)

    def _create_scenario_comparison_chart(self, scenario_dir: Path, 
                                        rag_deadlocked: bool, banker_deadlocked: bool,
                                        rag_processes: List[int], banker_processes: List[int]):
        """Create algorithm comparison chart."""
        
        if self.language == 'persian':
            comparison_text = f"""
مقایسه الگوریتم‌های تشخیص
=======================

تحلیل نمودار تخصیص منابع (RAG):
- نتیجه: {'بن‌بست شناسایی شد' if rag_deadlocked else 'بدون بن‌بست'}
- فرآیندهای درگیر: {rag_processes if rag_deadlocked else 'هیچ'}
- روش: تشخیص چرخه در نمودار تخصیص منابع
- پیچیدگی: O(V + E) که V = گره‌ها، E = یال‌ها
- دقت: تشخیص مستقیم انتظار دایره‌ای

تحلیل الگوریتم بانکدار:
- نتیجه: {'بن‌بست شناسایی شد' if banker_deadlocked else 'بدون بن‌بست'}
- فرآیندهای درگیر: {banker_processes if banker_deadlocked else 'هیچ'}
- رویکرد: تحلیل حالت امن با استفاده از ماتریس‌های تخصیص
- پیچیدگی: O(m × n²) که m = منابع، n = فرآیندها
- دقت: تشخیص حالات ناامن که ممکن است به بن‌بست منجر شوند

خلاصه مقایسه:
- توافق الگوریتم‌ها: {'بله' if rag_deadlocked == banker_deadlocked else 'خیر'}
- سازگاری: {'بالا' if rag_deadlocked == banker_deadlocked else 'نیاز به بررسی'}

چرا از چندین الگوریتم استفاده کنیم؟
- دیدگاه‌های مختلف نسبت به همان مسئله
- RAG: تشخیص مستقیم چرخه (دقیق برای منابع تک نمونه)
- بانکدار: تحلیل پیشگیرانه (کار با نمونه‌های متعدد)
- اعتبارسنجی متقابل اعتماد به نتایج را افزایش می‌دهد
"""
        else:
            comparison_text = f"""
DETECTION ALGORITHM COMPARISON
============================

Resource Allocation Graph (RAG) Analysis:
- Result: {'DEADLOCK DETECTED' if rag_deadlocked else 'NO DEADLOCK'}
- Processes involved: {rag_processes if rag_deadlocked else 'None'}
- Method: Cycle detection in resource allocation graph
- Complexity: O(V + E) where V = nodes, E = edges
- Accuracy: Direct detection of circular wait

Banker's Algorithm Analysis:  
- Result: {'DEADLOCK DETECTED' if banker_deadlocked else 'NO DEADLOCK'}
- Processes involved: {banker_processes if banker_deadlocked else 'None'}
- Method: Safe state analysis using allocation matrices
- Complexity: O(m × n²) where m = resources, n = processes
- Accuracy: Detects unsafe states that may lead to deadlock

COMPARISON SUMMARY:
- Algorithms agree: {'YES' if rag_deadlocked == banker_deadlocked else 'NO'}
- Consistency: {'High' if rag_deadlocked == banker_deadlocked else 'Requires investigation'}

WHY USE MULTIPLE ALGORITHMS?
- Different perspectives on the same problem
- RAG: Direct cycle detection (exact for single-instance resources)
- Banker's: Preventive analysis (works with multiple instances)
- Cross-validation increases confidence in results
"""
        
        with open(scenario_dir / "algorithm_comparison.txt", 'w', encoding='utf-8') as f:
            f.write(comparison_text)
    
    def _create_resolution_summary(self, scenario_dir: Path, resolution_results: Dict[str, bool]):
        """Create resolution strategies summary."""
        
        if self.language == 'persian':
            summary_text = f"""
تحلیل راهبردهای حل بن‌بست
===========================

نتایج آزمایش راهبردها:
- خاتمه فرآیند: {'موفق' if resolution_results.get('termination', False) else 'ناموفق'}
- پیش‌گیری منبع: {'موفق' if resolution_results.get('preemption', False) else 'ناموفق'}  
- برگشت فرآیند: {'موفق' if resolution_results.get('rollback', False) else 'ناموفق'}

توضیح راهبردها:

1. خاتمه فرآیند:
   - رویکرد: کشتن یک یا چند فرآیند بن‌بست
   - مزایا: ساده، همیشه کار می‌کند اگر درست اعمال شود
   - معایب: از دست رفتن کار، احتمال فساد داده
   - مورد استفاده: وقتی راه‌اندازی مجدد فرآیند قابل قبول است

2. پیش‌گیری منبع:
   - رویکرد: مجبور کردن فرآیندها به رها کردن منابع
   - مزایا: فرآیندها می‌توانند پس از بازگشت منبع ادامه دهند
   - معایب: ممکن است نیاز به برگشت فرآیند داشته باشد، پیاده‌سازی پیچیده
   - مورد استفاده: وقتی منابع می‌توانند با امنیت پیش‌گیری شوند

3. برگشت فرآیند:
   - رویکرد: لغو عملیات فرآیند به نقطه کنترل امن
   - مزایا: بدون خاتمه فرآیند، می‌تواند عملیات را دوباره امتحان کند
   - معایب: نیاز به مکانیزم‌های نقطه کنترل، مدیریت حالت پیچیده
   - مورد استفاده: وقتی مکانیزم‌های برگشت موجود است

معیارهای انتخاب:
- هزینه خاتمه فرآیند در مقابل برگشت را در نظر بگیرید
- امکان‌پذیری پیش‌گیری منبع را ارزیابی کنید
- راهبرد با کمترین تأثیر سیستم را انتخاب کنید
- ممکن است نیاز به ترکیب چندین رویکرد باشد
"""
        else:
            summary_text = f"""
DEADLOCK RESOLUTION STRATEGIES ANALYSIS
======================================

Strategy Test Results:
- Process Termination: {'SUCCESS' if resolution_results.get('termination', False) else 'FAILED'}
- Resource Preemption: {'SUCCESS' if resolution_results.get('preemption', False) else 'FAILED'}  
- Process Rollback: {'SUCCESS' if resolution_results.get('rollback', False) else 'FAILED'}

STRATEGY EXPLANATIONS:

1. PROCESS TERMINATION:
   - Approach: Kill one or more deadlocked processes
   - Pros: Simple, always works if applied correctly
   - Cons: Loss of work, potential data corruption
   - Use case: When process restart is acceptable

2. RESOURCE PREEMPTION:
   - Approach: Force processes to release resources
   - Pros: Processes can continue after resource is returned
   - Cons: May require process rollback, complex implementation
   - Use case: When resources can be safely preempted

3. PROCESS ROLLBACK:
   - Approach: Undo process operations to a safe checkpoint
   - Pros: No process termination, can retry operations
   - Cons: Requires checkpointing, complex state management
   - Use case: When rollback mechanisms are available

SELECTION CRITERIA:
- Consider cost of process termination vs. rollback
- Evaluate resource preemption feasibility
- Choose strategy with minimum system impact
- May need to combine multiple approaches
"""
        
        with open(scenario_dir / "resolution_analysis.txt", 'w', encoding='utf-8') as f:
            f.write(summary_text)
    
    def _create_learning_guide(self, scenario_dir: Path, scenario_info: Dict, 
                             deadlock_detected: bool, deadlocked_processes: List[int]):
        """Create comprehensive learning guide for the scenario."""
        
        if self.language == 'persian':
            guide_text = f"""
راهنمای یادگیری: {scenario_info['name']}
{'=' * (17 + len(scenario_info['name']))}

نمای کلی سناریو:
{scenario_info['description']}

اهداف یادگیری:
"""
            for i, objective in enumerate(scenario_info['learning_objectives'], 1):
                guide_text += f"{i}. {objective}\n"
            
            guide_text += f"""

نتایج تحلیل:
- وضعیت بن‌بست: {'🔴 شناسایی شد' if deadlock_detected else '🟢 شناسایی نشد'}
"""
            
            if deadlock_detected:
                guide_text += f"- فرآیندهای آسیب‌دیده: {', '.join([f'P{pid}' for pid in deadlocked_processes])}\n"
            
            guide_text += f"""

مفاهیم کلیدی نشان داده شده:

1. نمودار تخصیص منابع (RAG):
   - نمایش تصویری روابط فرآیند-منبع
   - گره‌ها: فرآیندها (دایره‌ها) و منابع (مربع‌ها)
   - یال‌ها: تخصیص (منبع←فرآیند) و درخواست (فرآیند←منبع)
   - چرخه‌ها در RAG نشان‌دهنده بن‌بست احتمالی

2. شرایط بن‌بست (شرایط کافمن):
   - انحصار متقابل: منابع قابل اشتراک نیستند
   - نگهداری و انتظار: فرآیندها منابع نگه می‌دارند و درخواست می‌کنند
   - عدم پیش‌گیری: منابع نمی‌توانند به زور گرفته شوند
   - انتظار دایره ای : زنجیره دایره ای وابستگی منابع

3. راهبردهای تشخیص:
   - تحلیل نمودار تخصیص منابع
   - الگوریتم بانکدار برای تحلیل حالت امن
   - رویکردهای مبتنی بر ماتریس برای سیستم‌های پیچیده

سؤالات مطالعه:
1. آیا می‌توانید شناسایی کنید کدام شرط(های) کافمن حضور دارد؟
2. اگر یکی از شرایط بن‌بست را حذف کنیم چه اتفاقی می‌افتد؟
3. چگونه از وقوع این بن‌بست جلوگیری می‌کردید؟
4. کدام راهبرد حل در اینجا مناسب‌تر است؟
5. اندازه سیستم چگونه بر پیچیدگی تشخیص تأثیر می‌گذارد؟

کاربردهای عملی:
- مدیریت تراکنش‌های پایگاه داده
- زمان‌بندی منابع سیستم عامل
- طراحی پروتکل‌های شبکه
- هماهنگی سیستم‌های توزیع‌شده

کاوش بیشتر:
- تغییر نمونه‌های منابع و مشاهده تأثیرات
- آزمایش ترتیب‌های مختلف اجرای فرآیند
- در نظر گیری سناریوهای دنیای واقعی با الگوهای مشابه
- تحقیق الگوریتم‌های پیشگیری (بانکدار، wound-wait و غیره)
"""
        else:
            guide_text = f"""
LEARNING GUIDE: {scenario_info['name']}
{'=' * (16 + len(scenario_info['name']))}

SCENARIO OVERVIEW:
{scenario_info['description']}

LEARNING OBJECTIVES:
"""
            for i, objective in enumerate(scenario_info['learning_objectives'], 1):
                guide_text += f"{i}. {objective}\n"
            
            guide_text += f"""

ANALYSIS RESULTS:
- Deadlock Status: {'🔴 DETECTED' if deadlock_detected else '🟢 NOT DETECTED'}
"""
            
            if deadlock_detected:
                guide_text += f"- Affected Processes: {', '.join([f'P{pid}' for pid in deadlocked_processes])}\n"
            
            guide_text += f"""

KEY CONCEPTS DEMONSTRATED:

1. RESOURCE ALLOCATION GRAPH (RAG):
   - Visual representation of process-resource relationships
   - Nodes: Processes (circles) and Resources (squares)
   - Edges: Allocation (resource→process) and Request (process→resource)
   - Cycles in RAG indicate potential deadlocks

2. DEADLOCK CONDITIONS (Coffman Conditions):
   - Mutual Exclusion: Resources cannot be shared
   - Hold and Wait: Processes hold resources while requesting others
   - No Preemption: Resources cannot be forcibly taken away
   - Circular Wait: Circular chain of resource dependencies

3. DETECTION STRATEGIES:
   - Resource Allocation Graph analysis
   - Banker's algorithm for safe state analysis
   - Matrix-based approaches for complex systems

STUDY QUESTIONS:
1. Can you identify which Coffman condition(s) are present?
2. What would happen if we removed one of the deadlock conditions?
3. How would you prevent this deadlock from occurring?
4. Which resolution strategy would be most appropriate here?
5. How does system size affect detection complexity?

PRACTICAL APPLICATIONS:
- Database transaction management
- Operating system resource scheduling
- Network protocol design
- Distributed system coordination

FURTHER EXPLORATION:
- Try modifying resource instances and observe effects
- Experiment with different process execution orders
- Consider real-world scenarios with similar patterns
- Research prevention algorithms (banker's, wound-wait, etc.)
"""
        
        with open(scenario_dir / "learning_guide.txt", 'w', encoding='utf-8') as f:
            f.write(guide_text)
    
    def _generate_project_summary(self, project_results: Dict[str, Any]):
        """Generate comprehensive project summary."""
        
        # Count results
        total_scenarios = len(project_results['scenarios_run'])
        successful_scenarios = len([s for s in project_results['scenarios_run'] if s.get('status') == 'completed'])
        deadlock_scenarios = len([s for s in project_results['scenarios_run'] 
                                if s.get('status') == 'completed' and s.get('deadlock_detected')])
        
        project_results['summary_statistics'] = {
            'total_scenarios': total_scenarios,
            'successful_scenarios': successful_scenarios,
            'failed_scenarios': total_scenarios - successful_scenarios,
            'deadlock_scenarios': deadlock_scenarios,
            'safe_scenarios': successful_scenarios - deadlock_scenarios
        }
        
        # Create summary text
        if self.language == 'persian':
            summary_text = f"""
خلاصه پروژه شبیه‌سازی بن‌بست
===========================

جزئیات پروژه:
- تاریخ/زمان: {datetime.fromtimestamp(int(project_results['timestamp'][:8])).strftime('%Y-%m-%d')} در {project_results['timestamp'][9:11]}:{project_results['timestamp'][11:13]}:{project_results['timestamp'][13:15]}
- کل سناریوها: {total_scenarios}
- اجراهای موفق: {successful_scenarios}
- اجراهای ناموفق: {total_scenarios - successful_scenarios}
- تصویرسازی: {'فعال' if project_results['visualizer_available'] else 'غیرفعال'}

نمای کلی نتایج:
- بن‌بست شناسایی شد: {deadlock_scenarios} سناریو
- سیستم‌های امن: {successful_scenarios - deadlock_scenarios} سناریو
- نرخ موفقیت: {(successful_scenarios/total_scenarios)*100:.1f}%

جزئیات سناریو:
"""
            
            for scenario in project_results['scenarios_run']:
                if scenario.get('status') == 'completed':
                    status_icon = '🔴' if scenario.get('deadlock_detected') else '🟢'
                    deadlock_info = f" (فرآیندها: {scenario.get('deadlocked_processes', [])})" if scenario.get('deadlock_detected') else ""
                    summary_text += f"{status_icon} {scenario['name']}{deadlock_info}\n"
                else:
                    summary_text += f"❌ {scenario['name']} - ناموفق\n"
            
            summary_text += f"""

ارزش آموزشی:
این پروژه انواع مختلف سناریوهای بن‌بست و الگوریتم‌های تشخیص را نشان می‌دهد.
هر پوشه سناریو شامل:
- توضیحات آموزشی مناسب برای یادگیری
- تحلیل فنی و مقایسه الگوریتم‌ها
- راهنماهای یادگیری با سؤالات مطالعه
- خلاصه وضعیت سیستم"""

            if project_results['visualizer_available']:
                summary_text += "\n- نمایش‌های تصویری (نمودارهای تخصیص منابع)"

            summary_text += f"""

فایل‌های تولید شده: {len(project_results['generated_files'])} فایل در همه سناریوها

ترتیب مطالعه پیشنهادی:
1. simple_deadlock - یادگیری مفاهیم پایه
2. no_deadlock - درک حالات امن
3. dining_philosophers_3 - چند فرآیند مقیاس کوچک
4. dining_philosophers_5 - مسئله کلاسیک
5. complex_allocation - سناریوهای پیشرفته
6. chain_deadlock - الگوهای جایگزین
7. dining_philosophers_7 - تحلیل مقیاس بزرگ

{'''نکته: اگر می‌خواهید تصویرسازی کامل داشته باشید، دستور زیر را اجرا کنید:
  bash install_persian_fonts.sh
سپس دوباره اسکریپت را اجرا کنید.''' if not project_results['visualizer_available'] else ''}


"""
        else:
            summary_text = f"""
DEADLOCK SIMULATION PROJECT SUMMARY
==================================

Project Details:
- Date/Time: {datetime.fromtimestamp(int(project_results['timestamp'][:8])).strftime('%Y-%m-%d')} at {project_results['timestamp'][9:11]}:{project_results['timestamp'][11:13]}:{project_results['timestamp'][13:15]}
- Total Scenarios: {total_scenarios}
- Successful Runs: {successful_scenarios}
- Failed Runs: {total_scenarios - successful_scenarios}
- Visualization: {'Available' if project_results['visualizer_available'] else 'Disabled'}

Results Overview:
- Deadlock Detected: {deadlock_scenarios} scenarios
- Safe Systems: {successful_scenarios - deadlock_scenarios} scenarios
- Success Rate: {(successful_scenarios/total_scenarios)*100:.1f}%

SCENARIO DETAILS:
"""
            
            for scenario in project_results['scenarios_run']:
                if scenario.get('status') == 'completed':
                    status_icon = '🔴' if scenario.get('deadlock_detected') else '🟢'
                    deadlock_info = f" (Processes: {scenario.get('deadlocked_processes', [])})" if scenario.get('deadlock_detected') else ""
                    summary_text += f"{status_icon} {scenario['name']}{deadlock_info}\n"
                else:
                    summary_text += f"❌ {scenario['name']} - FAILED\n"
            
            summary_text += f"""

EDUCATIONAL VALUE:
This project demonstrates various deadlock scenarios and detection algorithms.
Each scenario folder contains:
- Educational explanations suitable for learning
- Technical analysis and algorithm comparisons
- Learning guides with study questions
- System state summaries"""

            if project_results['visualizer_available']:
                summary_text += "\n- Visual representations (Resource Allocation Graphs)"

            summary_text += f"""

FILES GENERATED: {len(project_results['generated_files'])} files across all scenarios

RECOMMENDED STUDY ORDER:
1. simple_deadlock - Learn basic concepts
2. no_deadlock - Understand safe states  
3. dining_philosophers_3 - Small-scale multi-process
4. dining_philosophers_5 - Classic problem
5. complex_allocation - Advanced scenarios
6. chain_deadlock - Alternative patterns
7. dining_philosophers_7 - Large-scale analysis

{'''Note: For full visualization support, run:
  bash install_persian_fonts.sh
Then re-run the script.''' if not project_results['visualizer_available'] else ''}

Happy Learning! 🎓
"""
        
        # Save summary
        with open(self.project_dir / "project_summary.txt", 'w', encoding='utf-8') as f:
            f.write(summary_text)
        
        # Save JSON results
        with open(self.project_dir / "project_results.json", 'w', encoding='utf-8') as f:
            json.dump(project_results, f, indent=2, ensure_ascii=False)
    
    def _create_project_index(self, project_results: Dict[str, Any]):
        """Create HTML index file with RTL support for Persian."""
        
        if self.language == 'persian':
            self._create_persian_index(project_results)
        else:
            self._create_english_index(project_results)
    
    def _create_persian_index(self, project_results: Dict[str, Any]):
        """Create Persian RTL HTML index file."""
        
        html_content = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نتایج پروژه شبیه‌سازی بن‌بست</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100..900&display=swap');
        
        body {{
            font-family: 'Vazirmatn', 'Tahoma', 'Arial Unicode MS', sans-serif;
            line-height: 1.8;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
            direction: rtl;
            text-align: right;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .summary {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .warning-box {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .scenario-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }}
        .scenario-card {{
            background: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-right: 5px solid #667eea;
        }}
        .scenario-card.deadlock {{
            border-right-color: #e74c3c;
        }}
        .scenario-card.safe {{
            border-right-color: #27ae60;
        }}
        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .status-deadlock {{
            background-color: #e74c3c;
            color: white;
        }}
        .status-safe {{
            background-color: #27ae60;
            color: white;
        }}
        .file-list {{
            list-style: none;
            padding: 0;
        }}
        .file-list a {{
            text-decoration: none;
            color: #3498db;
            font-size: 0.9em;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .stat-label {{
            font-size: 0.9em;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎓 پروژه آموزشی شبیه‌سازی بن‌بست</h1>
        <p>تولید شده در {datetime.now().strftime('%d %B %Y')} در ساعت {datetime.now().strftime('%H:%M')}</p>
    </div>

    {f'''<div class="warning-box">
        ⚠️ <strong>توجه:</strong> تصویرسازی غیرفعال است. برای فعال‌سازی تصویرسازی کامل:
        <br>1. دستور <code>bash install_persian_fonts.sh</code> را اجرا کنید
        <br>2. سپس دوباره اسکریپت اصلی را اجرا کنید
    </div>''' if not project_results['visualizer_available'] else ''}

    <div class="summary">
        <h2>📊 نمای کلی پروژه</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0;">
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center;">
                <div class="stat-number">{project_results['summary_statistics']['total_scenarios']}</div>
                <div class="stat-label">کل سناریوها</div>
            </div>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center;">
                <div class="stat-number">{project_results['summary_statistics']['deadlock_scenarios']}</div>
                <div class="stat-label">موارد بن‌بست</div>
            </div>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center;">
                <div class="stat-number">{project_results['summary_statistics']['safe_scenarios']}</div>
                <div class="stat-label">سیستم‌های امن</div>
            </div>
            <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; text-align: center;">
                <div class="stat-number">{len(project_results['generated_files'])}</div>
                <div class="stat-label">فایل‌های تولید شده</div>
            </div>
        </div>
        
        <h3>📁 فایل‌های پروژه:</h3>
        <ul class="file-list">
            <li><a href="project_summary.txt">📄 خلاصه کامل پروژه</a></li>
            <li><a href="project_results.json">📊 نتایج فنی (JSON)</a></li>
        </ul>
    </div>

    <h2>🔬 نتایج سناریوها</h2>
    <div class="scenario-grid">
"""
        
        for scenario in project_results['scenarios_run']:
            if scenario.get('status') == 'completed':
                card_class = 'deadlock' if scenario.get('deadlock_detected') else 'safe'
                status_class = 'status-deadlock' if scenario.get('deadlock_detected') else 'status-safe'
                status_text = 'بن‌بست شناسایی شد' if scenario.get('deadlock_detected') else 'سیستم امن'
                
                deadlock_info = ""
                if scenario.get('deadlock_detected'):
                    processes = scenario.get('deadlocked_processes', [])
                    deadlock_info = f"<br><strong>آسیب‌دیده:</strong> {', '.join([f'P{pid}' for pid in processes])}"
                
                scenario_description = self.scenarios[scenario['scenario_id']]['description']
                
                html_content += f"""
        <div class="scenario-card {card_class}">
            <div style="font-size: 1.2em; font-weight: bold; margin-bottom: 10px; color: #2c3e50;">{scenario['name']}</div>
            <span class="status-badge {status_class}">{status_text}</span>
            <p>{scenario_description}{deadlock_info}</p>
            
            <h4>📁 فایل‌های تولید شده:</h4>
            <ul class="file-list">
                <li><a href="{scenario['scenario_directory']}/system_state_summary.txt">📊 خلاصه وضعیت سیستم</a></li>
                <li><a href="{scenario['scenario_directory']}/learning_guide.txt">🎓 راهنمای یادگیری</a></li>
                <li><a href="{scenario['scenario_directory']}/algorithm_comparison.txt">⚖️ مقایسه الگوریتم‌ها</a></li>"""
                
                if scenario.get('deadlock_detected'):
                    html_content += f"""
                <li><a href="{scenario['scenario_directory']}/resolution_analysis.txt">🛠️ تحلیل راه‌حل</a></li>"""
                
                # Add visualization links if available
                if project_results['visualizer_available']:
                    html_content += f"""
                <li><a href="{scenario['scenario_directory']}/resource_allocation_graph.png">📊 نمودار تخصیص منابع</a></li>
                <li><a href="{scenario['scenario_directory']}/system_state.png">📈 وضعیت سیستم</a></li>
                <li><a href="{scenario['scenario_directory']}/allocation_matrix.png">📋 ماتریس تخصیص</a></li>"""
                
                html_content += """
            </ul>
        </div>"""
        
        html_content += """
    </div>

    <div class="summary" style="margin-top: 30px;">
        <h2>🎯 نحوه استفاده از این مطالب</h2>
        <ol>
            <li><strong>با راهنماهای یادگیری شروع کنید:</strong> هر سناریو دارای راهنمای جامع یادگیری است.</li>
            <li><strong>خلاصه وضعیت سیستم را بررسی کنید:</strong> درک دقیق وضعیت فرآیندها و منابع.</li>
            <li><strong>الگوریتم‌ها را مقایسه کنید:</strong> ببینید روش‌های مختلف تشخیص چگونه کار می‌کنند.</li>
            <li><strong>راهبردهای حل را مطالعه کنید:</strong> یاد بگیرید کی و چگونه رویکردهای مختلف را اعمال کنید.</li>
        </ol>
        
        <h3>🎓 ارزش آموزشی</h3>
        <p>این مطالب برای موارد زیر طراحی شده‌اند:</p>
        <ul>
            <li>دانشجویان علوم کامپیوتر که در حال یادگیری سیستم‌های عامل هستند</li>
            <li>مربیانی که مفاهیم بن‌بست را تدریس می‌کنند</li>
            <li>هر کسی که علاقه‌مند به درک هماهنگی سیستم است</li>
        </ul>
    </div>

    <footer style="text-align: center; margin-top: 40px; color: #666; font-size: 0.9em;">
        <p>تولید شده توسط شبیه‌ساز آموزشی بن‌بست • {datetime.now().year}</p>
    </footer>
</body>
</html>"""
        
        with open(self.project_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(html_content)

    def _create_english_index(self, project_results: Dict[str, Any]):
        """Create English HTML index file."""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Deadlock Simulation Project Results</title>
    <style>
        body {{
            font-family: 'Georgia', serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .summary {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}
        .warning-box {{
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎓 Deadlock Simulation Educational Project</h1>
        <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
    </div>

    {f'''<div class="warning-box">
        ⚠️ <strong>Notice:</strong> Visualization is disabled. For full visualization support:
        <br>1. Run <code>bash install_persian_fonts.sh</code>
        <br>2. Then re-run the main script
    </div>''' if not project_results['visualizer_available'] else ''}

    <div class="summary">
        <h2>📊 Project Overview</h2>
        <p>All educational materials have been generated successfully, even without full visualization support.</p>
        
        <h3>📁 Project Files:</h3>
        <ul>
            <li><a href="project_summary.txt">📄 Complete Project Summary</a></li>
            <li><a href="project_results.json">📊 Technical Results (JSON)</a></li>
        </ul>
    </div>

    <h2>🔬 Scenario Results</h2>
    <div class="scenario-grid">
"""
        
        for scenario in project_results['scenarios_run']:
            if scenario.get('status') == 'completed':
                card_class = 'deadlock' if scenario.get('deadlock_detected') else 'safe'
                status_class = 'status-deadlock' if scenario.get('deadlock_detected') else 'status-safe'
                status_text = 'DEADLOCK DETECTED' if scenario.get('deadlock_detected') else 'SYSTEM SAFE'
                
                deadlock_info = ""
                if scenario.get('deadlock_detected'):
                    processes = scenario.get('deadlocked_processes', [])
                    deadlock_info = f"<br><strong>Affected:</strong> {', '.join([f'P{pid}' for pid in processes])}"
                
                scenario_description = self.scenarios[scenario['scenario_id']]['description']
                
                html_content += f"""
        <div class="scenario-card {card_class}">
            <div style="font-size: 1.2em; font-weight: bold; margin-bottom: 10px; color: #2c3e50;">{scenario['name']}</div>
            <span class="status-badge {status_class}">{status_text}</span>
            <p>{scenario_description}{deadlock_info}</p>
            
            <h4>📁 Generated Files:</h4>
            <ul class="file-list">
                <li><a href="{scenario['scenario_directory']}/system_state_summary.txt">📊 System State Summary</a></li>
                <li><a href="{scenario['scenario_directory']}/learning_guide.txt">🎓 Learning Guide</a></li>
                <li><a href="{scenario['scenario_directory']}/algorithm_comparison.txt">⚖️ Algorithm Comparison</a></li>"""
                
                if scenario.get('deadlock_detected'):
                    html_content += f"""
                <li><a href="{scenario['scenario_directory']}/resolution_analysis.txt">🛠️ Resolution Analysis</a></li>"""
                
                # Add visualization links if available
                if project_results['visualizer_available']:
                    html_content += f"""
                <li><a href="{scenario['scenario_directory']}/resource_allocation_graph.png">📊 Resource Allocation Graph</a></li>
                <li><a href="{scenario['scenario_directory']}/system_state.png">📈 System State</a></li>
                <li><a href="{scenario['scenario_directory']}/allocation_matrix.png">📋 Allocation Matrix</a></li>"""
                
                html_content += """
            </ul>
        </div>"""
        
        html_content += """
    </div>

    <div class="summary" style="margin-top: 30px;">
        <h2>🎯 نحوه استفاده از این مطالب</h2>
        <ol>
            <li><strong>با راهنماهای یادگیری شروع کنید:</strong> هر سناریو دارای راهنمای جامع یادگیری است.</li>
            <li><strong>خلاصه وضعیت سیستم را بررسی کنید:</strong> درک دقیق وضعیت فرآیندها و منابع.</li>
            <li><strong>الگوریتم‌ها را مقایسه کنید:</strong> ببینید روش‌های مختلف تشخیص چگونه کار می‌کنند.</li>
            <li><strong>راهبردهای حل را مطالعه کنید:</strong> یاد بگیرید کی و چگونه رویکردهای مختلف را اعمال کنید.</li>
        </ol>
        
        <h3>🎓 ارزش آموزشی</h3>
        <p>این مطالب برای موارد زیر طراحی شده‌اند:</p>
        <ul>
            <li>دانشجویان علوم کامپیوتر که در حال یادگیری سیستم‌های عامل هستند</li>
            <li>مربیانی که مفاهیم بن‌بست را تدریس می‌کنند</li>
            <li>هر کسی که علاقه‌مند به درک هماهنگی سیستم است</li>
        </ul>
    </div>

    <footer style="text-align: center; margin-top: 40px; color: #666; font-size: 0.9em;">
        <p>تولید شده توسط شبیه‌ساز آموزشی بن‌بست • {datetime.now().year}</p>
    </footer>
</body>
</html>"""
        
        with open(self.project_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(html_content)


def main():
    """Main function to run educational tests with improved error handling."""
    parser = argparse.ArgumentParser(
        description='اجرای تست‌های آموزشی شبیه‌سازی بن‌بست - نسخه اصلاح شده',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
مثال‌ها:
  python persian_test_runner_fixed.py                                    # اجرای همه سناریوها
  python persian_test_runner_fixed.py --output-dir ./my_results         # پوشه خروجی سفارشی  
  python persian_test_runner_fixed.py --scenarios simple_deadlock,dining_philosophers_5  # سناریوهای خاص
  python persian_test_runner_fixed.py --language english               # زبان انگلیسی

سناریوهای موجود:
  - simple_deadlock: بن‌بست ساده دو فرآیندی
  - dining_philosophers_3: فیلسوفان غذاخور کوچک
  - dining_philosophers_5: فیلسوفان غذاخور کلاسیک
  - dining_philosophers_7: فیلسوفان غذاخور بزرگ
  - complex_allocation: تخصیص چند منبعه
  - no_deadlock: حالت امن سیستم
  - chain_deadlock: الگوی زنجیره‌ای وابستگی

نکته: اگر هشدارهای فونت می‌بینید، دستور زیر را اجرا کنید:
  bash install_persian_fonts.sh
        """
    )
    
    parser.add_argument('--output-dir', '-o', default='educational_results',
                       help='پوشه اصلی خروجی نتایج')
    parser.add_argument('--scenarios', '-s', 
                       help='فهرست سناریوها جدا شده با کاما')
    parser.add_argument('--language', '-l', choices=['persian', 'english'], default='persian',
                       help='زبان خروجی (persian یا english)')
    
    args = parser.parse_args()
    
    # Parse scenarios
    selected_scenarios = None
    if args.scenarios:
        selected_scenarios = [s.strip() for s in args.scenarios.split(',')]
    
    # Create and run test runner
    runner = PersianEducationalTestRunner(args.output_dir, args.language)
    
    try:
        results = runner.run_all_scenarios(selected_scenarios)
        
        if args.language == 'persian':
            print(f"\n{'='*70}")
            print(f"🎉 موفقیت: مطالب آموزشی با موفقیت تولید شد!")
            print(f"📁 محل: {results['project_directory']}")
            print(f"📊 سناریوها: {results['summary_statistics']['successful_scenarios']} تکمیل شد")
            print(f"📄 فایل‌ها: {len(results['generated_files'])} فایل آموزشی ایجاد شد")
            print(f"🌐 مشاهده: فایل {results['project_directory']}/index.html را در مرورگر باز کنید")
            if not results['visualizer_available']:
                print(f"💡 برای تصویرسازی کامل: bash install_persian_fonts.sh")
            print(f"{'='*70}")
        else:
            print(f"\n{'='*70}")
            print(f"🎉 SUCCESS: Educational materials generated successfully!")
            print(f"📁 Location: {results['project_directory']}")
            print(f"📊 Scenarios: {results['summary_statistics']['successful_scenarios']} completed")
            print(f"📄 Files: {len(results['generated_files'])} educational files created")
            print(f"🌐 View: Open {results['project_directory']}/index.html in your browser")
            if not results['visualizer_available']:
                print(f"💡 For full visualization: bash install_persian_fonts.sh")
            print(f"{'='*70}")
        
        return 0
        
    except KeyboardInterrupt:
        if args.language == 'persian':
            print(f"\n⏹️ پروژه توسط کاربر متوقف شد")
        else:
            print(f"\n⏹️ Project interrupted by user")
        return 1
    except Exception as e:
        if args.language == 'persian':
            print(f"\n❌ پروژه ناموفق: {e}")
        else:
            print(f"\n❌ Project failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())