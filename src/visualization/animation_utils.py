"""
Complete Animation Utilities for Enhanced Deadlock Visualizer

This module provides utility classes and functions for creating smooth animations,
managing different animation types, and handling performance optimization for
dynamic visualizations.

File location: src/visualization/animation_utils.py
"""

import numpy as np
import time
import math
from enum import Enum
from typing import Dict, List, Tuple, Optional, Callable, Any
from dataclasses import dataclass
from collections import deque
import threading
import logging

class LayoutType(Enum):
    """Available layout algorithms for visualization."""
    SPRING = "spring"
    CIRCULAR = "circular"
    HIERARCHICAL = "hierarchical"
    GRID = "grid"
    KAMADA_KAWAI = "kamada_kawai"
    SHELL = "shell"
    SPECTRAL = "spectral"
    PLANAR = "planar"
    RANDOM = "random"
    BIPARTITE = "bipartite"

class AnimationType(Enum):
    """Types of animations available for dynamic visualizations."""
    FADE = "fade"
    SLIDE = "slide" 
    SCALE = "scale"
    ROTATE = "rotate"
    BOUNCE = "bounce"
    PULSE = "pulse"
    GLOW = "glow"
    SHAKE = "shake"
    SPIRAL = "spiral"
    WAVE = "wave"

class EasingFunction(Enum):
    """Easing functions for smooth animations."""
    LINEAR = "linear"
    EASE_IN = "ease_in"
    EASE_OUT = "ease_out"
    EASE_IN_OUT = "ease_in_out"
    BOUNCE_IN = "bounce_in"
    BOUNCE_OUT = "bounce_out"
    ELASTIC_IN = "elastic_in"
    ELASTIC_OUT = "elastic_out"
    BACK_IN = "back_in"
    BACK_OUT = "back_out"

@dataclass
class AnimationFrame:
    """Represents a single frame in an animation sequence."""
    timestamp: float
    alpha: float
    scale: float
    rotation: float
    offset_x: float
    offset_y: float
    color_intensity: float
    metadata: Dict[str, Any]

@dataclass
class AnimationState:
    """Current state of an animation."""
    start_time: float
    duration: float
    animation_type: AnimationType
    easing_function: EasingFunction
    loop: bool
    reverse: bool
    current_frame: int
    total_frames: int
    is_playing: bool
    is_paused: bool

class AnimationUtils:
    """
    Comprehensive utility class for handling animations in the deadlock visualizer.
    
    Provides:
    - Smooth interpolation functions
    - Animation timing and sequencing
    - Performance optimization
    - Frame generation and caching
    """
    
    def __init__(self, fps: int = 30, cache_size: int = 1000):
        """
        Initialize animation utilities.
        
        Args:
            fps: Target frames per second
            cache_size: Maximum number of cached animation frames
        """
        self.fps = fps
        self.frame_duration = 1.0 / fps
        self.cache_size = cache_size
        
        # Animation state management
        self.active_animations: Dict[str, AnimationState] = {}
        self.frame_cache: Dict[str, deque] = {}
        
        # Performance monitoring
        self.frame_times: deque = deque(maxlen=100)
        self.dropped_frames = 0
        
        # Threading for smooth animations
        self.animation_thread = None
        self.stop_event = threading.Event()
        
        # Logging
        self.logger = logging.getLogger(__name__)
    
    # =================================================================
    # EASING FUNCTIONS
    # =================================================================
    
    @staticmethod
    def linear(t: float) -> float:
        """Linear interpolation (no easing)."""
        return t
    
    @staticmethod
    def ease_in_quad(t: float) -> float:
        """Quadratic ease-in."""
        return t * t
    
    @staticmethod
    def ease_out_quad(t: float) -> float:
        """Quadratic ease-out."""
        return 1 - (1 - t) * (1 - t)
    
    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """Quadratic ease-in-out."""
        if t < 0.5:
            return 2 * t * t
        return 1 - pow(-2 * t + 2, 2) / 2
    
    @staticmethod
    def ease_in_cubic(t: float) -> float:
        """Cubic ease-in."""
        return t * t * t
    
    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """Cubic ease-out."""
        return 1 - pow(1 - t, 3)
    
    @staticmethod
    def ease_in_out_cubic(t: float) -> float:
        """Cubic ease-in-out."""
        if t < 0.5:
            return 4 * t * t * t
        return 1 - pow(-2 * t + 2, 3) / 2
    
    @staticmethod
    def bounce_out(t: float) -> float:
        """Bounce ease-out."""
        n1 = 7.5625
        d1 = 2.75
        
        if t < 1 / d1:
            return n1 * t * t
        elif t < 2 / d1:
            t -= 1.5 / d1
            return n1 * t * t + 0.75
        elif t < 2.5 / d1:
            t -= 2.25 / d1
            return n1 * t * t + 0.9375
        else:
            t -= 2.625 / d1
            return n1 * t * t + 0.984375
    
    @staticmethod
    def bounce_in(t: float) -> float:
        """Bounce ease-in."""
        return 1 - AnimationUtils.bounce_out(1 - t)
    
    @staticmethod
    def elastic_out(t: float) -> float:
        """Elastic ease-out."""
        c4 = (2 * math.pi) / 3
        
        if t == 0:
            return 0
        elif t == 1:
            return 1
        else:
            return pow(2, -10 * t) * math.sin((t * 10 - 0.75) * c4) + 1
    
    @staticmethod
    def elastic_in(t: float) -> float:
        """Elastic ease-in."""
        c4 = (2 * math.pi) / 3
        
        if t == 0:
            return 0
        elif t == 1:
            return 1
        else:
            return -pow(2, 10 * t - 10) * math.sin((t * 10 - 10.75) * c4)
    
    @staticmethod
    def back_out(t: float) -> float:
        """Back ease-out."""
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)
    
    @staticmethod
    def back_in(t: float) -> float:
        """Back ease-in."""
        c1 = 1.70158
        c3 = c1 + 1
        return c3 * t * t * t - c1 * t * t
    
    def get_easing_function(self, easing_type: EasingFunction) -> Callable[[float], float]:
        """Get the easing function by type."""
        easing_map = {
            EasingFunction.LINEAR: self.linear,
            EasingFunction.EASE_IN: self.ease_in_quad,
            EasingFunction.EASE_OUT: self.ease_out_quad,
            EasingFunction.EASE_IN_OUT: self.ease_in_out_quad,
            EasingFunction.BOUNCE_IN: self.bounce_in,
            EasingFunction.BOUNCE_OUT: self.bounce_out,
            EasingFunction.ELASTIC_IN: self.elastic_in,
            EasingFunction.ELASTIC_OUT: self.elastic_out,
            EasingFunction.BACK_IN: self.back_in,
            EasingFunction.BACK_OUT: self.back_out
        }
        return easing_map.get(easing_type, self.linear)
    
    # =================================================================
    # ANIMATION FRAME GENERATION
    # =================================================================
    
    def generate_fade_frame(self, t: float, easing_func: Callable[[float], float]) -> AnimationFrame:
        """Generate a fade animation frame."""
        eased_t = easing_func(t)
        alpha = 0.3 + 0.7 * (math.sin(2 * math.pi * eased_t) + 1) / 2
        
        return AnimationFrame(
            timestamp=time.time(),
            alpha=alpha,
            scale=1.0,
            rotation=0.0,
            offset_x=0.0,
            offset_y=0.0,
            color_intensity=1.0,
            metadata={'type': 'fade', 't': t, 'eased_t': eased_t}
        )
    
    def generate_pulse_frame(self, t: float, easing_func: Callable[[float], float]) -> AnimationFrame:
        """Generate a pulse animation frame."""
        eased_t = easing_func(t)
        scale = 0.8 + 0.4 * (math.sin(2 * math.pi * eased_t * 2) + 1) / 2
        alpha = 0.7 + 0.3 * (math.sin(2 * math.pi * eased_t * 2) + 1) / 2
        
        return AnimationFrame(
            timestamp=time.time(),
            alpha=alpha,
            scale=scale,
            rotation=0.0,
            offset_x=0.0,
            offset_y=0.0,
            color_intensity=1.0 + 0.3 * (math.sin(2 * math.pi * eased_t * 2) + 1) / 2,
            metadata={'type': 'pulse', 't': t, 'eased_t': eased_t}
        )
    
    def generate_bounce_frame(self, t: float, easing_func: Callable[[float], float]) -> AnimationFrame:
        """Generate a bounce animation frame."""
        eased_t = easing_func(t)
        
        # Bounce vertically
        bounce_height = 20 * abs(math.sin(math.pi * eased_t * 3))
        offset_y = -bounce_height if math.sin(math.pi * eased_t * 3) > 0 else 0
        
        # Slight scale change during bounce
        scale = 1.0 + 0.1 * abs(math.sin(math.pi * eased_t * 3))
        
        return AnimationFrame(
            timestamp=time.time(),
            alpha=1.0,
            scale=scale,
            rotation=0.0,
            offset_x=0.0,
            offset_y=offset_y,
            color_intensity=1.0,
            metadata={'type': 'bounce', 't': t, 'eased_t': eased_t}
        )
    
    def generate_rotate_frame(self, t: float, easing_func: Callable[[float], float]) -> AnimationFrame:
        """Generate a rotation animation frame."""
        eased_t = easing_func(t)
        rotation = 360 * eased_t  # Full rotation
        
        return AnimationFrame(
            timestamp=time.time(),
            alpha=1.0,
            scale=1.0,
            rotation=rotation,
            offset_x=0.0,
            offset_y=0.0,
            color_intensity=1.0,
            metadata={'type': 'rotate', 't': t, 'eased_t': eased_t}
        )
    
    def generate_glow_frame(self, t: float, easing_func: Callable[[float], float]) -> AnimationFrame:
        """Generate a glow animation frame."""
        eased_t = easing_func(t)
        
        # Pulsating glow effect
        glow_intensity = 1.0 + 0.8 * (math.sin(2 * math.pi * eased_t * 1.5) + 1) / 2
        alpha = 0.8 + 0.2 * (math.sin(2 * math.pi * eased_t * 1.5) + 1) / 2
        
        return AnimationFrame(
            timestamp=time.time(),
            alpha=alpha,
            scale=1.0,
            rotation=0.0,
            offset_x=0.0,
            offset_y=0.0,
            color_intensity=glow_intensity,
            metadata={'type': 'glow', 't': t, 'eased_t': eased_t}
        )
    
    def generate_shake_frame(self, t: float, easing_func: Callable[[float], float]) -> AnimationFrame:
        """Generate a shake animation frame."""
        eased_t = easing_func(t)
        
        # Random shake with decreasing intensity
        shake_intensity = 10 * (1 - eased_t)
        offset_x = shake_intensity * (np.random.random() - 0.5) * 2
        offset_y = shake_intensity * (np.random.random() - 0.5) * 2
        
        return AnimationFrame(
            timestamp=time.time(),
            alpha=1.0,
            scale=1.0,
            rotation=0.0,
            offset_x=offset_x,
            offset_y=offset_y,
            color_intensity=1.0,
            metadata={'type': 'shake', 't': t, 'eased_t': eased_t}
        )
    
    def generate_spiral_frame(self, t: float, easing_func: Callable[[float], float]) -> AnimationFrame:
        """Generate a spiral animation frame."""
        eased_t = easing_func(t)
        
        # Spiral motion
        radius = 30 * eased_t
        angle = 4 * math.pi * eased_t
        offset_x = radius * math.cos(angle)
        offset_y = radius * math.sin(angle)
        
        # Rotation follows the spiral
        rotation = math.degrees(angle)
        
        return AnimationFrame(
            timestamp=time.time(),
            alpha=1.0,
            scale=1.0,
            rotation=rotation,
            offset_x=offset_x,
            offset_y=offset_y,
            color_intensity=1.0,
            metadata={'type': 'spiral', 't': t, 'eased_t': eased_t}
        )
    
    def generate_wave_frame(self, t: float, easing_func: Callable[[float], float]) -> AnimationFrame:
        """Generate a wave animation frame."""
        eased_t = easing_func(t)
        
        # Wave motion
        wave_amplitude = 15
        wave_frequency = 3
        offset_y = wave_amplitude * math.sin(2 * math.pi * wave_frequency * eased_t)
        
        # Scale varies with wave
        scale = 1.0 + 0.2 * math.sin(2 * math.pi * wave_frequency * eased_t)
        
        return AnimationFrame(
            timestamp=time.time(),
            alpha=1.0,
            scale=scale,
            rotation=0.0,
            offset_x=0.0,
            offset_y=offset_y,
            color_intensity=1.0,
            metadata={'type': 'wave', 't': t, 'eased_t': eased_t}
        )
    
    def generate_animation_frame(self, animation_type: AnimationType, t: float, 
                               easing_func: Callable[[float], float]) -> AnimationFrame:
        """Generate an animation frame based on the animation type."""
        generators = {
            AnimationType.FADE: self.generate_fade_frame,
            AnimationType.PULSE: self.generate_pulse_frame,
            AnimationType.BOUNCE: self.generate_bounce_frame,
            AnimationType.ROTATE: self.generate_rotate_frame,
            AnimationType.GLOW: self.generate_glow_frame,
            AnimationType.SHAKE: self.generate_shake_frame,
            AnimationType.SPIRAL: self.generate_spiral_frame,
            AnimationType.WAVE: self.generate_wave_frame
        }
        
        generator = generators.get(animation_type, self.generate_fade_frame)
        return generator(t, easing_func)
    
    # =================================================================
    # ANIMATION MANAGEMENT
    # =================================================================
    
    def create_animation(self, animation_id: str, animation_type: AnimationType,
                        duration: float, easing_function: EasingFunction = EasingFunction.LINEAR,
                        loop: bool = True, reverse: bool = False) -> str:
        """
        Create a new animation.
        
        Args:
            animation_id: Unique identifier for the animation
            animation_type: Type of animation to create
            duration: Duration in seconds
            easing_function: Easing function to use
            loop: Whether to loop the animation
            reverse: Whether to reverse the animation
            
        Returns:
            str: Animation ID
        """
        total_frames = int(duration * self.fps)
        
        animation_state = AnimationState(
            start_time=time.time(),
            duration=duration,
            animation_type=animation_type,
            easing_function=easing_function,
            loop=loop,
            reverse=reverse,
            current_frame=0,
            total_frames=total_frames,
            is_playing=False,
            is_paused=False
        )
        
        self.active_animations[animation_id] = animation_state
        self.frame_cache[animation_id] = deque(maxlen=self.cache_size)
        
        # Pre-generate some frames for smooth playback
        self._pregenerate_frames(animation_id)
        
        return animation_id
    
    def _pregenerate_frames(self, animation_id: str, num_frames: int = 30):
        """Pre-generate frames for smooth animation playback."""
        if animation_id not in self.active_animations:
            return
        
        animation = self.active_animations[animation_id]
        easing_func = self.get_easing_function(animation.easing_function)
        cache = self.frame_cache[animation_id]
        
        for i in range(min(num_frames, animation.total_frames)):
            t = i / animation.total_frames
            frame = self.generate_animation_frame(animation.animation_type, t, easing_func)
            cache.append(frame)
    
    def play_animation(self, animation_id: str):
        """Start playing an animation."""
        if animation_id in self.active_animations:
            self.active_animations[animation_id].is_playing = True
            self.active_animations[animation_id].is_paused = False
            self.active_animations[animation_id].start_time = time.time()
    
    def pause_animation(self, animation_id: str):
        """Pause an animation."""
        if animation_id in self.active_animations:
            self.active_animations[animation_id].is_paused = True
    
    def stop_animation(self, animation_id: str):
        """Stop an animation."""
        if animation_id in self.active_animations:
            self.active_animations[animation_id].is_playing = False
            self.active_animations[animation_id].current_frame = 0
    
    def remove_animation(self, animation_id: str):
        """Remove an animation completely."""
        if animation_id in self.active_animations:
            del self.active_animations[animation_id]
        if animation_id in self.frame_cache:
            del self.frame_cache[animation_id]
    
    def get_current_frame(self, animation_id: str) -> Optional[AnimationFrame]:
        """Get the current frame for an animation."""
        if animation_id not in self.active_animations:
            return None
        
        animation = self.active_animations[animation_id]
        
        if not animation.is_playing or animation.is_paused:
            return None
        
        # Calculate current time in animation
        current_time = time.time() - animation.start_time
        
        if animation.loop:
            # Loop the animation
            current_time = current_time % animation.duration
        elif current_time > animation.duration:
            # Animation finished
            animation.is_playing = False
            return None
        
        # Calculate frame number
        t = current_time / animation.duration
        
        if animation.reverse:
            t = 1.0 - t
        
        # Try to get from cache first
        cache = self.frame_cache[animation_id]
        frame_index = int(t * animation.total_frames)
        
        if frame_index < len(cache):
            return cache[frame_index]
        
        # Generate frame on demand
        easing_func = self.get_easing_function(animation.easing_function)
        return self.generate_animation_frame(animation.animation_type, t, easing_func)
    
    # =================================================================
    # PERFORMANCE MONITORING
    # =================================================================
    
    def start_performance_monitoring(self):
        """Start monitoring animation performance."""
        self.frame_times.clear()
        self.dropped_frames = 0
    
    def record_frame_time(self, frame_time: float):
        """Record the time taken to render a frame."""
        self.frame_times.append(frame_time)
        
        # Check for dropped frames
        if frame_time > self.frame_duration * 1.5:
            self.dropped_frames += 1
    
    def get_performance_stats(self) -> Dict[str, float]:
        """Get performance statistics."""
        if not self.frame_times:
            return {
                'avg_frame_time': 0,
                'avg_fps': 0,
                'dropped_frames': 0,
                'frame_drop_rate': 0
            }
        
        avg_frame_time = sum(self.frame_times) / len(self.frame_times)
        avg_fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
        frame_drop_rate = self.dropped_frames / len(self.frame_times) * 100
        
        return {
            'avg_frame_time': avg_frame_time,
            'avg_fps': avg_fps,
            'dropped_frames': self.dropped_frames,
            'frame_drop_rate': frame_drop_rate
        }
    
    # =================================================================
    # UTILITY FUNCTIONS
    # =================================================================
    
    @staticmethod
    def interpolate(start: float, end: float, t: float) -> float:
        """Linear interpolation between two values."""
        return start + (end - start) * t
    
    @staticmethod
    def interpolate_color(start_color: Tuple[float, float, float], 
                         end_color: Tuple[float, float, float], t: float) -> Tuple[float, float, float]:
        """Interpolate between two RGB colors."""
        r = AnimationUtils.interpolate(start_color[0], end_color[0], t)
        g = AnimationUtils.interpolate(start_color[1], end_color[1], t)
        b = AnimationUtils.interpolate(start_color[2], end_color[2], t)
        return (r, g, b)
    
    @staticmethod
    def clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
        """Clamp a value between min and max."""
        return max(min_val, min(max_val, value))
    
    @staticmethod
    def smoothstep(edge0: float, edge1: float, x: float) -> float:
        """Smooth interpolation function."""
        t = AnimationUtils.clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
        return t * t * (3.0 - 2.0 * t)
    
    def cleanup(self):
        """Clean up resources and stop all animations."""
        self.stop_event.set()
        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_thread.join()
        
        self.active_animations.clear()
        self.frame_cache.clear()
        self.frame_times.clear()

# Factory function for easy animation creation
def create_animation_utils(fps: int = 30, cache_size: int = 1000) -> AnimationUtils:
    """
    Factory function to create AnimationUtils instance.
    
    Args:
        fps: Target frames per second
        cache_size: Maximum cached frames
        
    Returns:
        AnimationUtils: Configured animation utilities instance
    """
    return AnimationUtils(fps=fps, cache_size=cache_size)

# Predefined animation configurations
ANIMATION_PRESETS = {
    'deadlock_alert': {
        'type': AnimationType.PULSE,
        'duration': 2.0,
        'easing': EasingFunction.EASE_IN_OUT,
        'loop': True
    },
    'process_waiting': {
        'type': AnimationType.FADE,
        'duration': 3.0,
        'easing': EasingFunction.LINEAR,
        'loop': True
    },
    'resolution_success': {
        'type': AnimationType.BOUNCE,
        'duration': 1.5,
        'easing': EasingFunction.BOUNCE_OUT,
        'loop': False
    },
    'system_error': {
        'type': AnimationType.SHAKE,
        'duration': 0.8,
        'easing': EasingFunction.LINEAR,
        'loop': False
    },
    'resource_highlight': {
        'type': AnimationType.GLOW,
        'duration': 2.5,
        'easing': EasingFunction.EASE_IN_OUT,
        'loop': True
    }
}

# Usage example and testing
if __name__ == "__main__":
    print("🎬 Animation Utils Module")
    print("=" * 40)
    
    # Create animation utilities
    anim_utils = AnimationUtils(fps=30)
    
    # Test animation creation
    deadlock_anim = anim_utils.create_animation(
        "deadlock_pulse",
        AnimationType.PULSE,
        duration=2.0,
        easing_function=EasingFunction.EASE_IN_OUT,
        loop=True
    )
    
    print(f"✅ Created animation: {deadlock_anim}")
    
    # Test frame generation
    anim_utils.play_animation(deadlock_anim)
    frame = anim_utils.get_current_frame(deadlock_anim)
    
    if frame:
        print(f"📊 Sample frame: Alpha={frame.alpha:.2f}, Scale={frame.scale:.2f}")
    
    # Test performance monitoring
    anim_utils.start_performance_monitoring()
    anim_utils.record_frame_time(0.033)  # 30 FPS
    stats = anim_utils.get_performance_stats()
    
    print(f"⚡ Performance: {stats['avg_fps']:.1f} FPS")
    
    # Cleanup
    anim_utils.cleanup()
    
    print("✅ Animation utils module loaded successfully!")