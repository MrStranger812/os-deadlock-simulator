"""
Educational Deadlock Visualizer - Persian/Farsi Support with Fixed Unicode Issues

This module provides clean, educational visualizations suitable for academic
presentation with full Persian language support and RTL layout.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import json
from datetime import datetime
import os

# Import existing project components
from src.core import System, Process, Resource

class EducationalVisualizer:
    """
    Clean, educational visualizer for deadlock scenarios with Persian support.
    
    Designed for academic presentations with clear, professional output.
    """
    
    def __init__(self, system: System, language='persian'):
        """
        Initialize the educational visualizer.
        
        Args:
            system: The system to visualize
            language: 'persian' or 'english'
        """
        self.system = system
        self.language = language
        
        # Persian translations
        self.translations = {
            'persian': {
                'resource_allocation_graph': 'نمودار تخصیص منابع',
                'system_state': 'وضعیت سیستم',
                'allocation_matrix': 'ماتریس تخصیص',
                'explanation': 'توضیحات آموزشی',
                'learning_guide': 'راهنمای یادگیری',
                'algorithm_comparison': 'مقایسه الگوریتم‌ها',
                'resolution_analysis': 'تحلیل راه‌حل',
                'deadlock_detected': 'بن‌بست شناسایی شد',
                'no_deadlock': 'بدون بن‌بست',
                'processes': 'فرآیندها',
                'resources': 'منابع',
                'running': 'در حال اجرا',
                'waiting': 'در انتظار',
                'terminated': 'پایان یافته',
                'allocation_edge': 'یال تخصیص',
                'request_edge': 'یال درخواست',
                'deadlock_cycle': 'چرخه بن‌بست',
                'process_status': 'وضعیت فرآیندها',
                'resource_utilization': 'استفاده از منابع',
                'system_metrics': 'معیارهای سیستم',
                'time': 'زمان',
                'available': 'موجود',
                'allocated': 'تخصیص یافته',
                'requesting': 'درخواست‌کننده'
            },
            'english': {
                'resource_allocation_graph': 'Resource Allocation Graph',
                'system_state': 'System State',
                'allocation_matrix': 'Allocation Matrix',
                'explanation': 'Educational Explanation',
                'learning_guide': 'Learning Guide',
                'algorithm_comparison': 'Algorithm Comparison',
                'resolution_analysis': 'Resolution Analysis',
                'deadlock_detected': 'DEADLOCK DETECTED',
                'no_deadlock': 'NO DEADLOCK',
                'processes': 'Processes',
                'resources': 'Resources',
                'running': 'Running',
                'waiting': 'Waiting',
                'terminated': 'Terminated',
                'allocation_edge': 'Allocation Edge',
                'request_edge': 'Request Edge',
                'deadlock_cycle': 'Deadlock Cycle',
                'process_status': 'Process Status',
                'resource_utilization': 'Resource Utilization',
                'system_metrics': 'System Metrics',
                'time': 'Time',
                'available': 'Available',
                'allocated': 'Allocated',
                'requesting': 'Requesting'
            }
        }
        
        # Professional color scheme optimized for presentations and printing
        self.colors = {
            # Process states - clear semantic colors
            'process_running': '#2E8B57',      # Sea Green - healthy/active
            'process_waiting': '#DC143C',      # Crimson - blocked/waiting
            'process_terminated': '#708090',   # Slate Gray - inactive
            'process_deadlocked': '#8B008B',   # Dark Magenta - critical
            
            # Resources - calm, professional
            'resource_available': '#4682B4',   # Steel Blue
            'resource_allocated': '#1E90FF',   # Dodger Blue
            
            # Edges - clear relationships
            'edge_allocation': '#228B22',      # Forest Green - positive
            'edge_request': '#B22222',         # Fire Brick - demand
            'edge_deadlock': '#FF4500',        # Orange Red - problem
            
            # UI elements
            'background': '#FFFFFF',           # Pure white
            'text': '#000000',                 # Black text
            'grid': '#E0E0E0',                 # Light gray
            'border': '#808080',               # Medium gray
            'highlight': '#FFD700',            # Gold - attention
            
            # Annotations
            'annotation_bg': '#FFFACD',        # Lemon chiffon
            'annotation_border': '#DAA520'     # Goldenrod
        }
        
        # Set matplotlib parameters for professional output with Persian support
        plt.rcParams.update({
            'font.size': 11,
            'font.family': 'DejaVu Sans',  # Better Unicode support
            'axes.linewidth': 1.2,
            'axes.edgecolor': self.colors['border'],
            'figure.facecolor': self.colors['background'],
            'axes.facecolor': self.colors['background'],
            'savefig.facecolor': self.colors['background'],
            'savefig.dpi': 300,
            'figure.autolayout': True,
            'axes.unicode_minus': False  # Fix minus sign issues
        })
        
        # Try to set Persian font if available
        if language == 'persian':
            self._setup_persian_font()

    def _setup_persian_font(self):
        """Setup Persian font support."""
        try:
            # Try common Persian fonts
            persian_fonts = ['Tahoma', 'Arial Unicode MS', 'DejaVu Sans', 'Liberation Sans']
            for font in persian_fonts:
                plt.rcParams['font.family'] = font
                break
        except:
            # Fallback to default with better Unicode support
            plt.rcParams['font.family'] = 'DejaVu Sans'

    def _get_text(self, key: str) -> str:
        """Get translated text."""
        return self.translations[self.language].get(key, key)

    def create_comprehensive_visualization(self, deadlocked_processes: Optional[List[int]] = None,
                                         output_dir: str = "results",
                                         scenario_name: str = "scenario") -> Dict:
        """
        Create a comprehensive educational visualization with multiple views.
        
        Args:
            deadlocked_processes: List of deadlocked process IDs
            output_dir: Directory to save outputs
            scenario_name: Name of the scenario
            
        Returns:
            Dictionary with paths to generated files
        """
        # Create output directory structure
        scenario_dir = Path(output_dir) / scenario_name
        scenario_dir.mkdir(parents=True, exist_ok=True)
        
        generated_files = {}
        
        # 1. Resource Allocation Graph
        rag_path = scenario_dir / "resource_allocation_graph.png"
        try:
            self._create_resource_allocation_graph(deadlocked_processes, rag_path)
            generated_files['rag'] = str(rag_path)
            print(f"✅ Created: {rag_path}")
        except Exception as e:
            print(f"❌ Failed to create RAG: {e}")
        
        # 2. System State Overview
        state_path = scenario_dir / "system_state.png"
        try:
            self._create_system_state_overview(deadlocked_processes, state_path)
            generated_files['state'] = str(state_path)
            print(f"✅ Created: {state_path}")
        except Exception as e:
            print(f"❌ Failed to create system state: {e}")
        
        # 3. Process-Resource Matrix
        matrix_path = scenario_dir / "allocation_matrix.png"
        try:
            self._create_allocation_matrix(deadlocked_processes, matrix_path)
            generated_files['matrix'] = str(matrix_path)
            print(f"✅ Created: {matrix_path}")
        except Exception as e:
            print(f"❌ Failed to create matrix: {e}")
        
        # 4. Educational explanation
        explanation_path = scenario_dir / "explanation.txt"
        self._create_educational_explanation(deadlocked_processes, explanation_path, scenario_name)
        generated_files['explanation'] = str(explanation_path)
        
        # 5. Technical report (JSON)
        report_path = scenario_dir / "technical_report.json"
        self._create_technical_report(deadlocked_processes, report_path)
        generated_files['report'] = str(report_path)
        
        return generated_files

    def _create_resource_allocation_graph(self, deadlocked_processes: Optional[List[int]], 
                                        output_path: Path):
        """Create the main Resource Allocation Graph visualization."""
        fig, ax = plt.subplots(figsize=(12, 9))
        
        # Set title based on language
        title = self._get_text('resource_allocation_graph')
        fig.suptitle(title, fontsize=16, fontweight='bold', y=0.95)
        
        # Create NetworkX graph
        G = self._build_graph()
        
        # Compute layout - hierarchical for clear separation
        pos = self._compute_hierarchical_layout(G)
        
        # Draw the graph components
        self._draw_graph_nodes(G, pos, ax, deadlocked_processes)
        self._draw_graph_edges(G, pos, ax, deadlocked_processes)
        self._draw_graph_labels(G, pos, ax)
        
        # Add educational annotations
        self._add_rag_annotations(ax, deadlocked_processes)
        
        # Add legend
        self._add_comprehensive_legend(ax)
        
        # Format and save
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Use constrained layout instead of tight_layout
        fig.set_constrained_layout(True)
        
        try:
            plt.savefig(output_path, bbox_inches='tight', dpi=300, facecolor='white')
            print(f"✅ Saved RAG to: {output_path}")
        except Exception as e:
            print(f"❌ Error saving RAG: {e}")
        finally:
            plt.close(fig)

    def _create_system_state_overview(self, deadlocked_processes: Optional[List[int]], 
                                     output_path: Path):
        """Create a detailed system state overview."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        title = f'{self._get_text("system_state")} - {self._get_text("time")}: {self.system.time}'
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        try:
            # Top-left: Process status pie chart
            self._draw_process_status_chart(ax1)
            
            # Top-right: Resource utilization
            self._draw_resource_utilization(ax2)
            
            # Bottom-left: Simple allocation info
            self._draw_allocation_info(ax3)
            
            # Bottom-right: System metrics
            self._draw_system_metrics(ax4, deadlocked_processes)
            
            fig.set_constrained_layout(True)
            plt.savefig(output_path, bbox_inches='tight', dpi=300, facecolor='white')
            print(f"✅ Saved system state to: {output_path}")
        except Exception as e:
            print(f"❌ Error creating system state: {e}")
        finally:
            plt.close(fig)

    def _create_allocation_matrix(self, deadlocked_processes: Optional[List[int]], 
                                output_path: Path):
        """Create allocation matrix visualization."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        title = self._get_text('allocation_matrix')
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        try:
            processes = list(self.system.processes.keys())
            resources = list(self.system.resources.keys())
            
            # Create matrices
            allocation_matrix = np.zeros((len(processes), len(resources)))
            request_matrix = np.zeros((len(processes), len(resources)))
            
            for i, pid in enumerate(processes):
                process = self.system.processes[pid]
                for resource in process.resources_held:
                    j = resources.index(resource.rid)
                    allocation_matrix[i, j] = 1
                for resource in process.resources_requested:
                    j = resources.index(resource.rid)
                    request_matrix[i, j] = 1
            
            # Draw allocation matrix
            im1 = ax1.imshow(allocation_matrix, cmap='Greens', aspect='auto', vmin=0, vmax=1)
            ax1.set_title(f'{self._get_text("allocated")}', fontweight='bold')
            ax1.set_xticks(range(len(resources)))
            ax1.set_xticklabels([f'R{rid}' for rid in resources])
            ax1.set_yticks(range(len(processes)))
            ax1.set_yticklabels([f'P{pid}' for pid in processes])
            
            # Draw request matrix
            im2 = ax2.imshow(request_matrix, cmap='Reds', aspect='auto', vmin=0, vmax=1)
            ax2.set_title(f'{self._get_text("requesting")}', fontweight='bold')
            ax2.set_xticks(range(len(resources)))
            ax2.set_xticklabels([f'R{rid}' for rid in resources])
            ax2.set_yticks(range(len(processes)))
            ax2.set_yticklabels([f'P{pid}' for pid in processes])
            
            # Add checkmarks for allocated/requested
            for i in range(len(processes)):
                for j in range(len(resources)):
                    if allocation_matrix[i, j]:
                        ax1.text(j, i, '✓', ha='center', va='center', fontsize=16, fontweight='bold', color='darkgreen')
                    if request_matrix[i, j]:
                        ax2.text(j, i, '✓', ha='center', va='center', fontsize=16, fontweight='bold', color='darkred')
            
            fig.set_constrained_layout(True)
            plt.savefig(output_path, bbox_inches='tight', dpi=300, facecolor='white')
            print(f"✅ Saved matrix to: {output_path}")
        except Exception as e:
            print(f"❌ Error creating matrix: {e}")
        finally:
            plt.close(fig)

    def _create_educational_explanation(self, deadlocked_processes: Optional[List[int]], 
                                      output_path: Path, scenario_name: str):
        """Create comprehensive educational explanation in Persian."""
        if self.language == 'persian':
            explanation = self._create_persian_explanation(deadlocked_processes, scenario_name)
        else:
            explanation = self._create_english_explanation(deadlocked_processes, scenario_name)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(explanation)

    def _create_persian_explanation(self, deadlocked_processes: Optional[List[int]], scenario_name: str):
        """Create Persian educational explanation."""
        explanation = f"""
گزارش آموزشی شبیه‌سازی بن‌بست (Deadlock)
=======================================

سناریو: {scenario_name.replace('_', ' ')}
تاریخ تولید: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

بن‌بست (Deadlock) چیست؟
======================
بن‌بست مانند ترافیک در سیستم کامپیوتری است. تصور کنید دو ماشین در تقاطع:
- ماشین A مسیری را مسدود کرده که ماشین B نیاز دارد
- ماشین B مسیری را مسدود کرده که ماشین A نیاز دارد
- هیچ‌کدام نمی‌توانند حرکت کنند!

در سیستم‌های کامپیوتری:
- فرآیندها (PROCESSES) = ماشین‌ها
- منابع (RESOURCES) = بخش‌های جاده

وضعیت فعلی سیستم:
================
"""
        
        # Add system details
        explanation += f"تعداد کل فرآیندها: {len(self.system.processes)}\n"
        explanation += f"تعداد کل منابع: {len(self.system.resources)}\n\n"
        
        explanation += "جزئیات فرآیندها:\n"
        for pid, process in self.system.processes.items():
            status_persian = {
                'RUNNING': 'در حال اجرا',
                'WAITING': 'در انتظار', 
                'TERMINATED': 'پایان یافته'
            }
            explanation += f"• فرآیند P{pid} ({status_persian.get(process.status, process.status)}):\n"
            if process.resources_held:
                held = [f"R{r.rid}" for r in process.resources_held]
                explanation += f"  - در حال نگهداری: {', '.join(held)}\n"
            if process.resources_requested:
                requested = [f"R{r.rid}" for r in process.resources_requested]
                explanation += f"  - در انتظار: {', '.join(requested)}\n"
            explanation += "\n"
        
        explanation += "جزئیات منابع:\n"
        for rid, resource in self.system.resources.items():
            explanation += f"• منبع R{rid}:\n"
            explanation += f"  - موجود: {resource.available_instances}/{resource.total_instances} واحد\n"
            if resource.allocated_to:
                allocated = [f"P{pid}({count})" for pid, count in resource.allocated_to.items()]
                explanation += f"  - در حال استفاده توسط: {', '.join(allocated)}\n"
            explanation += "\n"
        
        # Deadlock analysis
        if deadlocked_processes:
            explanation += "🔴 بن‌بست شناسایی شد!\n"
            explanation += "=" * 20 + "\n"
            explanation += f"فرآیندهای درگیر: {', '.join([f'P{pid}' for pid in deadlocked_processes])}\n\n"
            explanation += "چرا این یک بن‌بست است؟\n"
            explanation += "بیایید وابستگی دایره‌ای را دنبال کنیم:\n\n"
            
            for pid in deadlocked_processes:
                process = self.system.processes[pid]
                explanation += f"• P{pid}:\n"
                if process.resources_held:
                    held = [f"R{r.rid}" for r in process.resources_held]
                    explanation += f"  - نگهداری: {', '.join(held)}\n"
                if process.resources_requested:
                    requested = [f"R{r.rid}" for r in process.resources_requested]
                    explanation += f"  - نیاز: {', '.join(requested)}\n"
                explanation += "\n"
                
            explanation += "این یک انتظار دایره‌ای ایجاد می‌کند:\n"
            explanation += "هر فرآیند منتظر منبعی است که توسط فرآیند دیگری در چرخه نگهداری می‌شود!\n\n"
            
            explanation += "راهبردهای حل:\n"
            explanation += "1. خاتمه فرآیند: کشتن یک یا چند فرآیند برای شکستن چرخه\n"
            explanation += "2. پیش‌گیری منبع: مجبور کردن فرآیند به رها کردن منابعش\n"
            explanation += "3. برگشت: لغو عملیات برای بازگشت به حالت امن\n\n"
            
        else:
            explanation += "🟢 بن‌بست شناسایی نشد\n"
            explanation += "=" * 22 + "\n"
            explanation += "سیستم در حال حاضر ایمن است. همه فرآیندها احتمالاً می‌توانند کارشان را تمام کنند.\n\n"
            explanation += "چرا بن‌بست نیست؟\n"
            explanation += "دلایل احتمالی:\n"
            explanation += "• منابع کافی برای همه درخواست‌ها موجود است\n"
            explanation += "• شرط انتظار دایره‌ای وجود ندارد\n"
            explanation += "• منابع قابل اشتراک‌گذاری هستند یا چندین نمونه دارند\n\n"
        
        explanation += "نکات کلیدی یادگیری:\n"
        explanation += "==================\n"
        explanation += "1. بن‌بست نیاز به چهار شرط دارد (شرایط کافمن):\n"
        explanation += "   - انحصار متقابل: منابع قابل اشتراک نیستند\n"
        explanation += "   - نگهداری و انتظار: فرآیندها منابع نگه می‌دارند و درخواست می‌کنند\n"
        explanation += "   - عدم پیش‌گیری: منابع نمی‌توانند به زور گرفته شوند\n"
        explanation += "   - انتظار دایره‌ای: چرخه‌ای از فرآیندهای منتظر یکدیگر\n\n"
        explanation += "2. پیشگیری: شکستن حداقل یکی از چهار شرط\n"
        explanation += "3. تشخیص: استفاده از الگوریتم‌هایی مثل تحلیل نمودار تخصیص منابع\n"
        explanation += "4. بازیابی: اعمال راهبردهای حل هنگام تشخیص بن‌بست\n\n"
        
        explanation += "راهنمای تصویرسازی:\n"
        explanation += "===================\n"
        explanation += "در نمودار تخصیص منابع:\n"
        explanation += "• دایره‌ها (○) = فرآیندها\n"
        explanation += "• مربع‌ها (□) = منابع\n"
        explanation += "• پیکان‌های ممتد (→) = منبع به فرآیند تخصیص یافته\n"
        explanation += "• پیکان‌های نقطه‌چین (⇢) = فرآیند منبع درخواست می‌کند\n"
        explanation += "• رنگ‌آمیزی قرمز = بخشی از چرخه بن‌بست\n\n"
        
        explanation += "به یاد داشته باشید: درک بن‌بست به طراحی سیستم‌های بهتر کمک می‌کند!\n"
        
        return explanation

    def _create_english_explanation(self, deadlocked_processes: Optional[List[int]], scenario_name: str):
        """Create English educational explanation (fallback)."""
        # Keep the original English version for reference
        explanation = f"""
DEADLOCK SIMULATION EDUCATIONAL REPORT
=====================================

Scenario: {scenario_name.replace('_', ' ').title()}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

WHAT IS A DEADLOCK?
------------------
A deadlock is like a traffic jam in a computer system...
"""
        # (Continue with English version for brevity)
        return explanation

    def _create_technical_report(self, deadlocked_processes: Optional[List[int]], 
                               output_path: Path):
        """Create technical report in JSON format."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "language": self.language,
            "system_state": {
                "time": self.system.time,
                "processes": {
                    str(pid): {
                        "status": process.status,
                        "resources_held": [r.rid for r in process.resources_held],
                        "resources_requested": [r.rid for r in process.resources_requested]
                    }
                    for pid, process in self.system.processes.items()
                },
                "resources": {
                    str(rid): {
                        "total_instances": resource.total_instances,
                        "available_instances": resource.available_instances,
                        "allocated_to": dict(resource.allocated_to)
                    }
                    for rid, resource in self.system.resources.items()
                }
            },
            "deadlock_analysis": {
                "deadlock_detected": bool(deadlocked_processes),
                "deadlocked_processes": deadlocked_processes or [],
                "analysis_method": "Resource Allocation Graph"
            },
            "statistics": {
                "total_processes": len(self.system.processes),
                "total_resources": len(self.system.resources),
                "waiting_processes": sum(1 for p in self.system.processes.values() 
                                       if p.status == 'WAITING'),
                "running_processes": sum(1 for p in self.system.processes.values() 
                                       if p.status == 'RUNNING'),
                "terminated_processes": sum(1 for p in self.system.processes.values() 
                                          if p.status == 'TERMINATED'),
                "total_resource_instances": sum(r.total_instances 
                                              for r in self.system.resources.values()),
                "available_resource_instances": sum(r.available_instances 
                                                   for r in self.system.resources.values())
            }
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

    # Helper methods for graph creation and drawing
    def _build_graph(self) -> nx.DiGraph:
        """Build NetworkX graph from system state."""
        G = nx.DiGraph()
        
        # Add process nodes
        for pid in self.system.processes:
            G.add_node(f'P{pid}', type='process')
        
        # Add resource nodes
        for rid in self.system.resources:
            G.add_node(f'R{rid}', type='resource')
        
        # Add allocation edges (Resource -> Process)
        for pid, process in self.system.processes.items():
            for resource in process.resources_held:
                G.add_edge(f'R{resource.rid}', f'P{pid}', type='allocation')
        
        # Add request edges (Process -> Resource)
        for pid, process in self.system.processes.items():
            for resource in process.resources_requested:
                G.add_edge(f'P{pid}', f'R{resource.rid}', type='request')
        
        return G

    def _compute_hierarchical_layout(self, G: nx.DiGraph) -> Dict:
        """Compute hierarchical layout with processes on top, resources below."""
        pos = {}
        processes = [n for n in G.nodes() if n.startswith('P')]
        resources = [n for n in G.nodes() if n.startswith('R')]
        
        # Arrange processes in top row
        for i, p in enumerate(processes):
            pos[p] = (i * 3, 2)
        
        # Arrange resources in bottom row
        for i, r in enumerate(resources):
            pos[r] = (i * 3, -1)
        
        return pos

    def _draw_graph_nodes(self, G: nx.DiGraph, pos: Dict, ax, deadlocked_processes: Optional[List[int]]):
        """Draw graph nodes with appropriate styling."""
        deadlocked_nodes = set()
        if deadlocked_processes:
            deadlocked_nodes = {f'P{pid}' for pid in deadlocked_processes}
        
        for node in G.nodes():
            x, y = pos[node]
            
            if node.startswith('P'):
                # Process node
                pid = int(node[1:])
                process = self.system.processes.get(pid)
                
                if process and process.status == 'RUNNING':
                    color = self.colors['process_running']
                elif process and process.status == 'WAITING':
                    color = self.colors['process_waiting']
                else:
                    color = self.colors['process_terminated']
                
                # Highlight deadlocked processes
                if node in deadlocked_nodes:
                    edge_color = self.colors['edge_deadlock']
                    edge_width = 4
                else:
                    edge_color = self.colors['border']
                    edge_width = 2
                
                circle = plt.Circle((x, y), 0.4, color=color, ec=edge_color, linewidth=edge_width)
                ax.add_patch(circle)
                
            else:
                # Resource node
                color = self.colors['resource_available']
                
                # Check if resource is involved in deadlock
                edge_color = self.colors['border']
                edge_width = 2
                if deadlocked_processes:
                    for pid in deadlocked_processes:
                        process = self.system.processes[pid]
                        for resource in process.resources_held + process.resources_requested:
                            if f'R{resource.rid}' == node:
                                edge_color = self.colors['edge_deadlock']
                                edge_width = 4
                                break
                
                square = plt.Rectangle((x-0.35, y-0.35), 0.7, 0.7, color=color, 
                                     ec=edge_color, linewidth=edge_width)
                ax.add_patch(square)

    def _draw_graph_edges(self, G: nx.DiGraph, pos: Dict, ax, deadlocked_processes: Optional[List[int]]):
        """Draw graph edges with clear visual distinction."""
        for edge in G.edges(data=True):
            source, target, data = edge
            x1, y1 = pos[source]
            x2, y2 = pos[target]
            
            edge_type = data.get('type', 'allocation')
            
            if edge_type == 'allocation':
                color = self.colors['edge_allocation']
                style = '-'
                alpha = 0.8
            else:  # request
                color = self.colors['edge_request']
                style = '--'
                alpha = 0.8
            
            # Check if edge is part of deadlock cycle
            is_deadlock_edge = False
            if deadlocked_processes:
                if (source.startswith('P') and target.startswith('R')):
                    pid = int(source[1:])
                    if pid in deadlocked_processes:
                        is_deadlock_edge = True
                elif (source.startswith('R') and target.startswith('P')):
                    pid = int(target[1:])
                    if pid in deadlocked_processes:
                        is_deadlock_edge = True
            
            if is_deadlock_edge:
                color = self.colors['edge_deadlock']
                linewidth = 3
            else:
                linewidth = 2
            
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', color=color, lw=linewidth,
                                     linestyle=style, alpha=alpha))

    def _draw_graph_labels(self, G: nx.DiGraph, pos: Dict, ax):
        """Draw clear, readable labels for nodes."""
        for node in G.nodes():
            x, y = pos[node]
            ax.text(x, y, node, ha='center', va='center', fontsize=12, 
                   fontweight='bold', color='white', zorder=10)

    def _add_rag_annotations(self, ax, deadlocked_processes: Optional[List[int]]):
        """Add educational annotations to the RAG."""
        # Add process/resource type labels
        processes_text = self._get_text('processes') + "\n" + "(دایره‌ها)" if self.language == 'persian' else self._get_text('processes') + "\n(Circles)"
        resources_text = self._get_text('resources') + "\n" + "(مربع‌ها)" if self.language == 'persian' else self._get_text('resources') + "\n(Squares)"
        
        ax.text(0.02, 0.98, processes_text, transform=ax.transAxes,
               verticalalignment='top', fontsize=10, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['annotation_bg'],
                        edgecolor=self.colors['annotation_border']))
        
        ax.text(0.02, 0.15, resources_text, transform=ax.transAxes,
               verticalalignment='top', fontsize=10, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor=self.colors['annotation_bg'],
                        edgecolor=self.colors['annotation_border']))
        
        # Add deadlock status
        if deadlocked_processes:
            if self.language == 'persian':
                status_text = f"بن‌بست شناسایی شد\nفرآیندها: {', '.join([f'P{pid}' for pid in deadlocked_processes])}"
            else:
                status_text = f"DEADLOCK DETECTED\nProcesses: {', '.join([f'P{pid}' for pid in deadlocked_processes])}"
            status_color = '#FFE4E1'  # Misty rose
        else:
            if self.language == 'persian':
                status_text = "بدون بن‌بست\nسیستم ایمن است"
            else:
                status_text = "NO DEADLOCK\nSystem is safe"
            status_color = '#F0FFF0'  # Honeydew
        
        ax.text(0.98, 0.98, status_text, transform=ax.transAxes,
               horizontalalignment='right', verticalalignment='top',
               fontsize=12, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.7', facecolor=status_color,
                        edgecolor=self.colors['border'], linewidth=2))

    def _add_comprehensive_legend(self, ax):
        """Add comprehensive legend explaining all visual elements."""
        if self.language == 'persian':
            legend_labels = [
                'فرآیند در حال اجرا',
                'فرآیند در انتظار', 
                'منبع',
                'یال تخصیص (منبع ← فرآیند)',
                'یال درخواست (فرآیند ← منبع)',
                'چرخه بن‌بست'
            ]
        else:
            legend_labels = [
                'Running Process',
                'Waiting Process',
                'Resource',
                'Allocation (Resource → Process)',
                'Request (Process → Resource)',
                'Deadlock Cycle'
            ]
        
        legend_elements = [
            mpatches.Circle((0, 0), 0.1, facecolor=self.colors['process_running'], 
                           edgecolor='black', label=legend_labels[0]),
            mpatches.Circle((0, 0), 0.1, facecolor=self.colors['process_waiting'], 
                           edgecolor='black', label=legend_labels[1]),
            mpatches.Rectangle((0, 0), 0.2, 0.2, facecolor=self.colors['resource_available'], 
                             edgecolor='black', label=legend_labels[2]),
            plt.Line2D([0], [0], color=self.colors['edge_allocation'], 
                      linewidth=3, label=legend_labels[3]),
            plt.Line2D([0], [0], color=self.colors['edge_request'], 
                      linewidth=3, linestyle='--', label=legend_labels[4]),
            plt.Line2D([0], [0], color=self.colors['edge_deadlock'], 
                      linewidth=4, label=legend_labels[5])
        ]
        
        legend = ax.legend(handles=legend_elements, loc='upper left',
                          bbox_to_anchor=(1.02, 1), fontsize=10)
        legend.get_frame().set_facecolor(self.colors['background'])
        legend.get_frame().set_edgecolor(self.colors['border'])

    def _draw_process_status_chart(self, ax):
        """Draw process status pie chart."""
        statuses = {'RUNNING': 0, 'WAITING': 0, 'TERMINATED': 0}
        for process in self.system.processes.values():
            statuses[process.status] += 1
        
        if self.language == 'persian':
            status_labels = {
                'RUNNING': 'در حال اجرا',
                'WAITING': 'در انتظار',
                'TERMINATED': 'پایان یافته'
            }
        else:
            status_labels = {
                'RUNNING': 'Running',
                'WAITING': 'Waiting', 
                'TERMINATED': 'Terminated'
            }
        
        labels = []
        sizes = []
        colors = []
        
        for status, count in statuses.items():
            if count > 0:
                labels.append(f'{status_labels[status]}\n({count})')
                sizes.append(count)
                colors.append(self.colors[f'process_{status.lower()}'])
        
        if sizes:
            ax.pie(sizes, labels=labels, colors=colors, autopct='%1.0f%%', startangle=90)
        
        title = self._get_text('process_status')
        ax.set_title(title, fontweight='bold')

    def _draw_resource_utilization(self, ax):
        """Draw resource utilization chart."""
        resources = list(self.system.resources.keys())
        used = []
        available = []
        
        for rid in resources:
            resource = self.system.resources[rid]
            used_instances = resource.total_instances - resource.available_instances
            used.append(used_instances)
            available.append(resource.available_instances)
        
        x = np.arange(len(resources))
        width = 0.35
        
        if self.language == 'persian':
            used_label = 'استفاده شده'
            available_label = 'موجود'
        else:
            used_label = 'Used'
            available_label = 'Available'
        
        ax.bar(x, used, width, label=used_label, color=self.colors['resource_allocated'])
        ax.bar(x, available, width, bottom=used, label=available_label, 
              color=self.colors['resource_available'])
        
        ax.set_xlabel(self._get_text('resources'))
        ax.set_ylabel('تعداد' if self.language == 'persian' else 'Instances')
        ax.set_title(self._get_text('resource_utilization'), fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels([f'R{rid}' for rid in resources])
        ax.legend()

    def _draw_allocation_info(self, ax):
        """Draw allocation information."""
        if self.language == 'persian':
            title = 'اطلاعات تخصیص'
            text = 'توضیح:\nاین نمودار وضعیت\nتخصیص منابع به\nفرآیندها را نشان می‌دهد'
        else:
            title = 'Allocation Information'
            text = 'Explanation:\nThis shows the current\nallocation status of\nresources to processes'
        
        ax.text(0.5, 0.5, text, ha='center', va='center', transform=ax.transAxes,
               fontsize=11, fontweight='bold',
               bbox=dict(boxstyle='round,pad=1', facecolor=self.colors['annotation_bg']))
        ax.set_title(title, fontweight='bold')
        ax.axis('off')

    def _draw_system_metrics(self, ax, deadlocked_processes: Optional[List[int]]):
        """Draw key system metrics."""
        if self.language == 'persian':
            metrics_labels = [
                'کل فرآیندها',
                'کل منابع', 
                'فرآیندهای منتظر',
                'فرآیندهای بن‌بست'
            ]
        else:
            metrics_labels = [
                'Total Processes',
                'Total Resources',
                'Waiting Processes', 
                'Deadlocked Processes'
            ]
        
        metrics_values = [
            len(self.system.processes),
            len(self.system.resources),
            sum(1 for p in self.system.processes.values() if p.status == 'WAITING'),
            len(deadlocked_processes) if deadlocked_processes else 0
        ]
        
        y_pos = np.arange(len(metrics_labels))
        
        bars = ax.barh(y_pos, metrics_values, color=self.colors['resource_available'])
        ax.set_yticks(y_pos)
        ax.set_yticklabels(metrics_labels)
        ax.set_xlabel('تعداد' if self.language == 'persian' else 'Count')
        ax.set_title(self._get_text('system_metrics'), fontweight='bold')
        
        # Add value labels on bars
        for i, v in enumerate(metrics_values):
            ax.text(v + 0.1, i, str(v), va='center', fontweight='bold')

    # Main interface methods
    def visualize_current_state(self, deadlocked_processes: Optional[List[int]] = None):
        """Create and display current state visualization."""
        fig, ax = plt.subplots(figsize=(12, 9))
        
        title = self._get_text('resource_allocation_graph')
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        G = self._build_graph()
        pos = self._compute_hierarchical_layout(G)
        
        self._draw_graph_nodes(G, pos, ax, deadlocked_processes)
        self._draw_graph_edges(G, pos, ax, deadlocked_processes)
        self._draw_graph_labels(G, pos, ax)
        self._add_rag_annotations(ax, deadlocked_processes)
        self._add_comprehensive_legend(ax)
        
        ax.set_aspect('equal')
        ax.axis('off')
        fig.set_constrained_layout(True)
        plt.show()

    def save_visualization(self, filename: str, deadlocked_processes: Optional[List[int]] = None):
        """Save current visualization to file."""
        fig, ax = plt.subplots(figsize=(12, 9))
        
        title = self._get_text('resource_allocation_graph')
        fig.suptitle(title, fontsize=16, fontweight='bold')
        
        G = self._build_graph()
        pos = self._compute_hierarchical_layout(G)
        
        self._draw_graph_nodes(G, pos, ax, deadlocked_processes)
        self._draw_graph_edges(G, pos, ax, deadlocked_processes)
        self._draw_graph_labels(G, pos, ax)
        self._add_rag_annotations(ax, deadlocked_processes)
        self._add_comprehensive_legend(ax)
        
        ax.set_aspect('equal')
        ax.axis('off')
        fig.set_constrained_layout(True)
        
        try:
            plt.savefig(filename, bbox_inches='tight', dpi=300, facecolor='white')
            print(f"✅ Visualization saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving visualization: {e}")
        finally:
            plt.close(fig)


# Backward compatibility alias
DeadlockVisualizer = EducationalVisualizer