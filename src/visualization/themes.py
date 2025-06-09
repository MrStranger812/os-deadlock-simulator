"""
Complete Color Themes and Styling for Enhanced Deadlock Visualizer

This module provides comprehensive theming support including:
- Multiple color schemes (light, dark, high contrast, colorblind-friendly)
- Dynamic theme switching
- Custom theme creation and validation
- Theme export/import functionality
- Accessibility compliance
- Professional styling presets

File location: src/visualization/themes.py
"""

import colorsys
import json
from typing import Dict, List, Tuple, Optional, Union
from enum import Enum
from dataclasses import dataclass, asdict
from pathlib import Path
import logging

class ThemeType(Enum):
    """Available theme categories."""
    LIGHT = "light"
    DARK = "dark"
    HIGH_CONTRAST = "high_contrast"
    COLORBLIND = "colorblind"
    CUSTOM = "custom"
    PROFESSIONAL = "professional"
    EDUCATIONAL = "educational"

@dataclass
class ColorPalette:
    """Represents a complete color palette for visualization."""
    # Process colors
    process_running: str
    process_waiting: str
    process_terminated: str
    process_deadlocked: str
    
    # Resource colors
    resource_available: str
    resource_allocated: str
    resource_contested: str
    
    # Edge colors
    edge_allocation: str
    edge_request: str
    edge_resolution: str
    edge_deadlock: str
    
    # Background and UI colors
    background: str
    paper: str
    surface: str
    primary: str
    secondary: str
    accent: str
    
    # Text colors
    text_primary: str
    text_secondary: str
    text_disabled: str
    text_on_primary: str
    
    # Status colors
    success: str
    warning: str
    error: str
    info: str
    
    # Interactive elements
    highlight: str
    selection: str
    hover: str
    focus: str
    
    # Grid and borders
    grid: str
    border: str
    divider: str
    
    # Special effects
    glow: str
    shadow: str
    overlay: str

@dataclass 
class ThemeMetadata:
    """Metadata for themes."""
    name: str
    description: str
    author: str
    version: str
    theme_type: ThemeType
    accessibility_rating: str  # A, AA, AAA
    supports_dark_mode: bool
    is_colorblind_friendly: bool
    tags: List[str]

class ColorThemes:
    """
    Comprehensive color theme manager for the deadlock visualizer.
    
    Provides multiple built-in themes, theme validation, custom theme creation,
    and accessibility compliance checking.
    """
    
    def __init__(self):
        """Initialize the theme manager with built-in themes."""
        self.themes: Dict[str, ColorPalette] = {}
        self.metadata: Dict[str, ThemeMetadata] = {}
        self.current_theme = "default"
        
        # Initialize built-in themes
        self._initialize_builtin_themes()
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
    
    def _initialize_builtin_themes(self):
        """Initialize all built-in color themes."""
        
        # =====================================================================
        # DEFAULT THEME (Light, Professional)
        # =====================================================================
        self.themes["default"] = ColorPalette(
            # Process colors - semantic and intuitive
            process_running="#2ecc71",      # Green - healthy/active
            process_waiting="#e74c3c",      # Red - blocked/waiting  
            process_terminated="#95a5a6",   # Gray - inactive
            process_deadlocked="#8e44ad",   # Purple - critical state
            
            # Resource colors - calm blues
            resource_available="#3498db",   # Blue - available
            resource_allocated="#2980b9",   # Darker blue - in use
            resource_contested="#e67e22",   # Orange - contested
            
            # Edge colors - clear relationships
            edge_allocation="#27ae60",      # Dark green - positive flow
            edge_request="#c0392b",         # Dark red - demand/tension
            edge_resolution="#16a085",      # Teal - solution
            edge_deadlock="#9b59b6",        # Purple - problem
            
            # Background and surfaces
            background="#ffffff",           # Pure white
            paper="#fafafa",               # Slightly off-white
            surface="#f5f5f5",             # Light surface
            primary="#3498db",             # Primary blue
            secondary="#95a5a6",           # Secondary gray
            accent="#e74c3c",              # Accent red
            
            # Text hierarchy
            text_primary="#2c3e50",        # Dark blue-gray
            text_secondary="#7f8c8d",      # Medium gray
            text_disabled="#bdc3c7",       # Light gray
            text_on_primary="#ffffff",     # White on primary
            
            # Status colors (standard semantic colors)
            success="#27ae60",             # Green
            warning="#f39c12",             # Orange
            error="#e74c3c",               # Red
            info="#3498db",                # Blue
            
            # Interactive states
            highlight="#f39c12",           # Orange highlight
            selection="#3498db",           # Blue selection
            hover="#ecf0f1",               # Light hover
            focus="#3498db",               # Blue focus ring
            
            # Structure elements
            grid="#ecf0f1",                # Very light gray
            border="#bdc3c7",              # Medium gray border
            divider="#ecf0f1",             # Light divider
            
            # Effects
            glow="#f39c12",                # Orange glow
            shadow="#000000",              # Black shadow
            overlay="#000000"              # Black overlay
        )
        
        self.metadata["default"] = ThemeMetadata(
            name="Default Light",
            description="Clean, professional light theme optimized for presentations and general use",
            author="Deadlock Visualizer Team", 
            version="1.0.0",
            theme_type=ThemeType.LIGHT,
            accessibility_rating="AA",
            supports_dark_mode=False,
            is_colorblind_friendly=False,
            tags=["professional", "clean", "presentation", "default"]
        )
        
        # =====================================================================
        # DARK THEME (Modern Dark UI)
        # =====================================================================
        self.themes["dark"] = ColorPalette(
            # Process colors - vibrant against dark background
            process_running="#00ff7f",      # Spring green - vibrant
            process_waiting="#ff4500",      # Orange red - attention
            process_terminated="#a9a9a9",   # Dark gray
            process_deadlocked="#ff69b4",   # Hot pink - critical
            
            # Resource colors - cool tones
            resource_available="#1e90ff",   # Dodger blue
            resource_allocated="#4169e1",   # Royal blue
            resource_contested="#ffa500",   # Orange
            
            # Edge colors - high contrast
            edge_allocation="#7fff00",      # Chartreuse - success
            edge_request="#ff1493",         # Deep pink - demand
            edge_resolution="#00ced1",      # Dark turquoise
            edge_deadlock="#da70d6",        # Orchid
            
            # Dark theme backgrounds
            background="#1a1a1a",           # Very dark
            paper="#2d2d2d",               # Dark surface
            surface="#3d3d3d",             # Elevated surface
            primary="#bb86fc",             # Purple primary
            secondary="#03dac6",           # Teal secondary
            accent="#cf6679",              # Pink accent
            
            # Dark theme text
            text_primary="#ffffff",        # White primary text
            text_secondary="#b3b3b3",      # Light gray secondary
            text_disabled="#666666",       # Medium gray disabled
            text_on_primary="#000000",     # Black on primary
            
            # Dark theme status
            success="#00ff7f",             # Bright green
            warning="#ffa500",             # Orange
            error="#ff4444",               # Bright red
            info="#00bfff",                # Deep sky blue
            
            # Dark theme interactive
            highlight="#ffd700",           # Gold highlight
            selection="#bb86fc",           # Purple selection
            hover="#404040",               # Dark hover
            focus="#bb86fc",               # Purple focus
            
            # Dark theme structure  
            grid="#404040",                # Dark grid
            border="#666666",              # Medium border
            divider="#404040",             # Dark divider
            
            # Dark theme effects
            glow="#ffd700",                # Gold glow
            shadow="#000000",              # Black shadow
            overlay="#000000"              # Black overlay
        )
        
        self.metadata["dark"] = ThemeMetadata(
            name="Dark Professional",
            description="Modern dark theme reducing eye strain with vibrant accent colors",
            author="Deadlock Visualizer Team",
            version="1.0.0", 
            theme_type=ThemeType.DARK,
            accessibility_rating="AA",
            supports_dark_mode=True,
            is_colorblind_friendly=False,
            tags=["dark", "modern", "eye-strain", "vibrant"]
        )
        
        # =====================================================================
        # COLORBLIND FRIENDLY THEME
        # =====================================================================
        self.themes["colorblind"] = ColorPalette(
            # Colorblind-safe process colors (avoiding red-green confusion)
            process_running="#0173b2",      # Blue - universally safe
            process_waiting="#de8f05",      # Orange - safe alternative to red
            process_terminated="#737373",   # Gray - neutral
            process_deadlocked="#cc78bc",   # Pink - distinctive
            
            # Colorblind-safe resource colors
            resource_available="#029e73",   # Green-blue - safe green
            resource_allocated="#56b4e9",   # Sky blue
            resource_contested="#e69f00",   # Orange
            
            # Colorblind-safe edges
            edge_allocation="#009e73",      # Blue-green
            edge_request="#d55e00",         # Vermillion
            edge_resolution="#0072b2",      # Blue
            edge_deadlock="#cc79a7",        # Rose pink
            
            # Standard backgrounds (colorblind-friendly)
            background="#ffffff",
            paper="#fafafa",
            surface="#f0f0f0",
            primary="#0173b2",
            secondary="#737373",
            accent="#de8f05",
            
            # High contrast text
            text_primary="#000000",
            text_secondary="#4d4d4d",
            text_disabled="#999999",
            text_on_primary="#ffffff",
            
            # Colorblind-safe status
            success="#009e73",             # Blue-green success
            warning="#e69f00",             # Orange warning
            error="#d55e00",               # Vermillion error
            info="#0173b2",                # Blue info
            
            # Accessible interactive
            highlight="#e69f00",           # Orange highlight
            selection="#0173b2",           # Blue selection
            hover="#f0f0f0",               # Light hover
            focus="#0173b2",               # Blue focus
            
            # Clear structure
            grid="#e0e0e0",
            border="#999999",
            divider="#e0e0e0",
            
            # Accessible effects
            glow="#e69f00",
            shadow="#000000",
            overlay="#000000"
        )
        
        self.metadata["colorblind"] = ThemeMetadata(
            name="Colorblind Accessible",
            description="Designed for deuteranopia, protanopia, and tritanopia accessibility",
            author="Accessibility Team",
            version="1.0.0",
            theme_type=ThemeType.COLORBLIND,
            accessibility_rating="AAA",
            supports_dark_mode=False,
            is_colorblind_friendly=True,
            tags=["accessibility", "colorblind", "universal", "inclusive"]
        )
        
        # =====================================================================
        # HIGH CONTRAST THEME
        # =====================================================================
        self.themes["high_contrast"] = ColorPalette(
            # Maximum contrast process colors
            process_running="#00ff00",      # Pure green
            process_waiting="#ff0000",      # Pure red
            process_terminated="#808080",   # Medium gray
            process_deadlocked="#ff00ff",   # Magenta
            
            # High contrast resources
            resource_available="#0000ff",   # Pure blue
            resource_allocated="#000080",   # Navy
            resource_contested="#ffff00",   # Yellow
            
            # Maximum contrast edges
            edge_allocation="#00ff00",      # Pure green
            edge_request="#ff0000",         # Pure red
            edge_resolution="#00ffff",      # Cyan
            edge_deadlock="#ff00ff",        # Magenta
            
            # High contrast backgrounds
            background="#ffffff",           # Pure white
            paper="#ffffff",               # Pure white
            surface="#f0f0f0",             # Very light gray
            primary="#000000",             # Pure black
            secondary="#808080",           # Medium gray
            accent="#ff0000",              # Pure red
            
            # Maximum contrast text
            text_primary="#000000",        # Pure black
            text_secondary="#404040",      # Dark gray
            text_disabled="#808080",       # Medium gray
            text_on_primary="#ffffff",     # Pure white
            
            # High contrast status
            success="#00ff00",             # Pure green
            warning="#ffff00",             # Pure yellow
            error="#ff0000",               # Pure red
            info="#0000ff",                # Pure blue
            
            # High contrast interactive
            highlight="#ffff00",           # Yellow highlight
            selection="#0000ff",           # Blue selection
            hover="#e0e0e0",               # Light gray hover
            focus="#ff0000",               # Red focus ring
            
            # Clear structure
            grid="#c0c0c0",                # Light gray grid
            border="#000000",              # Black border
            divider="#808080",             # Gray divider
            
            # High contrast effects
            glow="#ffff00",                # Yellow glow
            shadow="#000000",              # Black shadow
            overlay="#000000"              # Black overlay
        )
        
        self.metadata["high_contrast"] = ThemeMetadata(
            name="High Contrast",
            description="Maximum contrast theme for users with low vision or bright environments",
            author="Accessibility Team",
            version="1.0.0",
            theme_type=ThemeType.HIGH_CONTRAST,
            accessibility_rating="AAA",
            supports_dark_mode=False,
            is_colorblind_friendly=True,
            tags=["accessibility", "high-contrast", "low-vision", "bright"]
        )
        
        # =====================================================================
        # EDUCATIONAL THEME (Soft, friendly colors)
        # =====================================================================
        self.themes["educational"] = ColorPalette(
            # Gentle, educational colors
            process_running="#52c41a",      # Soft green
            process_waiting="#fa8c16",      # Soft orange
            process_terminated="#8c8c8c",   # Soft gray
            process_deadlocked="#eb2f96",   # Soft pink
            
            # Educational resource colors
            resource_available="#1890ff",   # Soft blue
            resource_allocated="#096dd9",   # Deeper blue
            resource_contested="#fa541c",   # Soft red-orange
            
            # Friendly edge colors
            edge_allocation="#73d13d",      # Light green
            edge_request="#ff7875",         # Light red
            edge_resolution="#40a9ff",      # Light blue
            edge_deadlock="#f759ab",        # Light pink
            
            # Warm, friendly backgrounds
            background="#fafafa",           # Warm white
            paper="#ffffff",               # Pure white
            surface="#f5f5f5",             # Light surface
            primary="#1890ff",             # Friendly blue
            secondary="#8c8c8c",           # Soft gray
            accent="#fa8c16",              # Warm orange
            
            # Readable text
            text_primary="#262626",        # Soft black
            text_secondary="#595959",      # Medium gray
            text_disabled="#bfbfbf",       # Light gray
            text_on_primary="#ffffff",     # White on primary
            
            # Educational status colors
            success="#52c41a",             # Success green
            warning="#fa8c16",             # Warning orange
            error="#ff4d4f",               # Error red
            info="#1890ff",                # Info blue
            
            # Gentle interactive
            highlight="#fadb14",           # Warm yellow
            selection="#bae7ff",           # Light blue
            hover="#f5f5f5",               # Light hover
            focus="#40a9ff",               # Blue focus
            
            # Soft structure
            grid="#f0f0f0",                # Very light grid
            border="#d9d9d9",              # Light border
            divider="#f0f0f0",             # Light divider
            
            # Gentle effects
            glow="#fadb14",                # Warm glow
            shadow="#00000020",            # Soft shadow
            overlay="#00000040"            # Light overlay
        )
        
        self.metadata["educational"] = ThemeMetadata(
            name="Educational Friendly",
            description="Soft, approachable colors perfect for teaching and learning environments",
            author="Education Team",
            version="1.0.0",
            theme_type=ThemeType.EDUCATIONAL,
            accessibility_rating="AA",
            supports_dark_mode=False,
            is_colorblind_friendly=False,
            tags=["educational", "friendly", "soft", "teaching", "learning"]
        )
        
        # =====================================================================
        # PROFESSIONAL PRESENTATION THEME
        # =====================================================================
        self.themes["professional"] = ColorPalette(
            # Corporate, professional colors
            process_running="#28a745",      # Professional green
            process_waiting="#dc3545",      # Professional red
            process_terminated="#6c757d",   # Professional gray
            process_deadlocked="#6f42c1",   # Professional purple
            
            # Business-appropriate resources
            resource_available="#007bff",   # Professional blue
            resource_allocated="#0056b3",   # Darker professional blue
            resource_contested="#fd7e14",   # Professional orange
            
            # Corporate edge colors
            edge_allocation="#20c997",      # Professional teal
            edge_request="#e83e8c",         # Professional pink
            edge_resolution="#17a2b8",      # Professional cyan
            edge_deadlock="#6f42c1",        # Professional purple
            
            # Corporate backgrounds
            background="#ffffff",           # Clean white
            paper="#f8f9fa",               # Light corporate gray
            surface="#e9ecef",             # Corporate surface
            primary="#007bff",             # Corporate blue
            secondary="#6c757d",           # Corporate gray
            accent="#dc3545",              # Corporate red
            
            # Professional text
            text_primary="#212529",        # Dark corporate
            text_secondary="#495057",      # Medium corporate
            text_disabled="#adb5bd",       # Light corporate
            text_on_primary="#ffffff",     # White on primary
            
            # Corporate status
            success="#28a745",             # Success green
            warning="#ffc107",             # Warning yellow
            error="#dc3545",               # Error red
            info="#17a2b8",                # Info cyan
            
            # Professional interactive
            highlight="#ffc107",           # Warning yellow highlight
            selection="#cce7ff",           # Light blue selection
            hover="#e9ecef",               # Light hover
            focus="#007bff",               # Blue focus
            
            # Clean structure
            grid="#dee2e6",                # Corporate grid
            border="#ced4da",              # Corporate border
            divider="#dee2e6",             # Corporate divider
            
            # Professional effects
            glow="#ffc107",                # Corporate glow
            shadow="#00000025",            # Subtle shadow
            overlay="#00000050"            # Professional overlay
        )
        
        self.metadata["professional"] = ThemeMetadata(
            name="Professional Presentation",
            description="Clean, corporate colors suitable for business presentations and reports",
            author="Business Team",
            version="1.0.0",
            theme_type=ThemeType.PROFESSIONAL,
            accessibility_rating="AA",
            supports_dark_mode=False,
            is_colorblind_friendly=False,
            tags=["professional", "corporate", "presentation", "business", "clean"]
        )
    
    # =========================================================================
    # THEME MANAGEMENT METHODS
    # =========================================================================
    
    def get_theme(self, theme_name: str) -> Optional[ColorPalette]:
        """
        Get a theme by name.
        
        Args:
            theme_name: Name of the theme to retrieve
            
        Returns:
            ColorPalette or None if theme doesn't exist
        """
        return self.themes.get(theme_name)
    
    def get_theme_dict(self, theme_name: str) -> Optional[Dict[str, str]]:
        """
        Get a theme as a dictionary (for backward compatibility).
        
        Args:
            theme_name: Name of the theme to retrieve
            
        Returns:
            Dictionary of color mappings or None
        """
        theme = self.get_theme(theme_name)
        if theme:
            return asdict(theme)
        return None
    
    def list_themes(self) -> List[str]:
        """Get a list of all available theme names."""
        return list(self.themes.keys())
    
    def get_theme_metadata(self, theme_name: str) -> Optional[ThemeMetadata]:
        """Get metadata for a specific theme."""
        return self.metadata.get(theme_name)
    
    def get_themes_by_type(self, theme_type: ThemeType) -> List[str]:
        """Get all themes of a specific type."""
        return [
            name for name, meta in self.metadata.items()
            if meta.theme_type == theme_type
        ]
    
    def get_accessible_themes(self, rating: str = "AA") -> List[str]:
        """Get themes that meet accessibility standards."""
        valid_ratings = {"A": 1, "AA": 2, "AAA": 3}
        min_rating = valid_ratings.get(rating, 2)
        
        return [
            name for name, meta in self.metadata.items()
            if valid_ratings.get(meta.accessibility_rating, 0) >= min_rating
        ]
    
    def get_colorblind_friendly_themes(self) -> List[str]:
        """Get themes that are colorblind-friendly."""
        return [
            name for name, meta in self.metadata.items()
            if meta.is_colorblind_friendly
        ]
    
    # =========================================================================
    # THEME CREATION AND CUSTOMIZATION
    # =========================================================================
    
    def create_custom_theme(self, name: str, base_theme: str = "default", 
                          modifications: Dict[str, str] = None) -> bool:
        """
        Create a custom theme based on an existing theme.
        
        Args:
            name: Name for the new custom theme
            base_theme: Base theme to start from
            modifications: Dictionary of color modifications
            
        Returns:
            bool: True if theme was created successfully
        """
        if base_theme not in self.themes:
            self.logger.error(f"Base theme '{base_theme}' not found")
            return False
        
        if name in self.themes:
            self.logger.warning(f"Theme '{name}' already exists, overwriting")
        
        # Start with base theme
        base_palette = self.themes[base_theme]
        custom_palette_dict = asdict(base_palette)
        
        # Apply modifications
        if modifications:
            for key, value in modifications.items():
                if key in custom_palette_dict:
                    if self.validate_color(value):
                        custom_palette_dict[key] = value
                    else:
                        self.logger.warning(f"Invalid color '{value}' for key '{key}'")
                else:
                    self.logger.warning(f"Unknown color key '{key}'")
        
        # Create new palette
        try:
            custom_palette = ColorPalette(**custom_palette_dict)
            self.themes[name] = custom_palette
            
            # Create metadata
            base_meta = self.metadata[base_theme]
            self.metadata[name] = ThemeMetadata(
                name=name,
                description=f"Custom theme based on {base_theme}",
                author="User",
                version="1.0.0",
                theme_type=ThemeType.CUSTOM,
                accessibility_rating="Unknown",
                supports_dark_mode=base_meta.supports_dark_mode,
                is_colorblind_friendly=False,  # Unknown for custom themes
                tags=["custom"] + base_meta.tags
            )
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to create custom theme: {e}")
            return False
    
    def validate_color(self, color: str) -> bool:
        """
        Validate a color string (hex, rgb, or named color).
        
        Args:
            color: Color string to validate
            
        Returns:
            bool: True if color is valid
        """
        # Check hex colors
        if color.startswith('#'):
            if len(color) == 7:  # #RRGGBB
                try:
                    int(color[1:], 16)
                    return True
                except ValueError:
                    return False
            elif len(color) == 4:  # #RGB
                try:
                    int(color[1:], 16)
                    return True
                except ValueError:
                    return False
        
        # Check rgb/rgba colors
        if color.startswith(('rgb(', 'rgba(')):
            # Basic validation - could be enhanced
            return ')' in color
        
        # Check named colors (basic list)
        named_colors = {
            'red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink',
            'brown', 'black', 'white', 'gray', 'grey', 'cyan', 'magenta'
        }
        
        return color.lower() in named_colors
    
    # =========================================================================
    # THEME OPERATIONS
    # =========================================================================
    
    def export_theme(self, theme_name: str, filepath: str) -> bool:
        """
        Export a theme to a JSON file.
        
        Args:
            theme_name: Name of theme to export
            filepath: Path to save the theme file
            
        Returns:
            bool: True if export was successful
        """
        if theme_name not in self.themes:
            self.logger.error(f"Theme '{theme_name}' not found")
            return False
        
        try:
            theme_data = {
                'palette': asdict(self.themes[theme_name]),
                'metadata': asdict(self.metadata[theme_name])
            }
            
            with open(filepath, 'w') as f:
                json.dump(theme_data, f, indent=2)
            
            self.logger.info(f"Theme '{theme_name}' exported to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export theme: {e}")
            return False
    
    def import_theme(self, filepath: str, theme_name: str = None) -> bool:
        """
        Import a theme from a JSON file.
        
        Args:
            filepath: Path to the theme file
            theme_name: Optional name for the imported theme
            
        Returns:
            bool: True if import was successful
        """
        try:
            with open(filepath, 'r') as f:
                theme_data = json.load(f)
            
            # Extract palette and metadata
            palette_data = theme_data.get('palette', {})
            metadata_data = theme_data.get('metadata', {})
            
            # Use provided name or fall back to metadata name
            name = theme_name or metadata_data.get('name', 'imported_theme')
            
            # Create palette
            palette = ColorPalette(**palette_data)
            self.themes[name] = palette
            
            # Create metadata
            metadata = ThemeMetadata(**metadata_data)
            metadata.name = name  # Ensure name matches
            self.metadata[name] = metadata
            
            self.logger.info(f"Theme imported as '{name}'")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to import theme: {e}")
            return False
    
    def duplicate_theme(self, source_theme: str, new_name: str) -> bool:
        """
        Duplicate an existing theme with a new name.
        
        Args:
            source_theme: Name of theme to duplicate
            new_name: Name for the duplicated theme
            
        Returns:
            bool: True if duplication was successful
        """
        if source_theme not in self.themes:
            self.logger.error(f"Source theme '{source_theme}' not found")
            return False
        
        if new_name in self.themes:
            self.logger.warning(f"Theme '{new_name}' already exists, overwriting")
        
        try:
            # Duplicate palette
            source_palette = self.themes[source_theme]
            self.themes[new_name] = ColorPalette(**asdict(source_palette))
            
            # Duplicate metadata
            source_metadata = self.metadata[source_theme]
            new_metadata = ThemeMetadata(**asdict(source_metadata))
            new_metadata.name = new_name
            new_metadata.description = f"Copy of {source_theme}"
            self.metadata[new_name] = new_metadata
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to duplicate theme: {e}")
            return False
    
    def remove_theme(self, theme_name: str) -> bool:
        """
        Remove a custom theme.
        
        Args:
            theme_name: Name of theme to remove
            
        Returns:
            bool: True if removal was successful
        """
        # Protect built-in themes
        builtin_themes = {"default", "dark", "colorblind", "high_contrast", 
                         "educational", "professional"}
        
        if theme_name in builtin_themes:
            self.logger.error(f"Cannot remove built-in theme '{theme_name}'")
            return False
        
        if theme_name not in self.themes:
            self.logger.error(f"Theme '{theme_name}' not found")
            return False
        
        try:
            del self.themes[theme_name]
            del self.metadata[theme_name]
            
            # Reset current theme if it was removed
            if self.current_theme == theme_name:
                self.current_theme = "default"
            
            self.logger.info(f"Theme '{theme_name}' removed")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to remove theme: {e}")
            return False
    
    # =========================================================================
    # ACCESSIBILITY AND ANALYSIS
    # =========================================================================
    
    def analyze_contrast(self, theme_name: str) -> Dict[str, float]:
        """
        Analyze color contrast ratios for a theme.
        
        Args:
            theme_name: Name of theme to analyze
            
        Returns:
            Dictionary of contrast ratios
        """
        if theme_name not in self.themes:
            return {}
        
        theme = self.themes[theme_name]
        
        def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
            """Convert hex color to RGB tuple."""
            hex_color = hex_color.lstrip('#')
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def relative_luminance(rgb: Tuple[int, int, int]) -> float:
            """Calculate relative luminance of an RGB color."""
            def linearize(component: int) -> float:
                c = component / 255.0
                return c / 12.92 if c <= 0.03928 else pow((c + 0.055) / 1.055, 2.4)
            
            r, g, b = map(linearize, rgb)
            return 0.2126 * r + 0.7152 * g + 0.0722 * b
        
        def contrast_ratio(color1: str, color2: str) -> float:
            """Calculate contrast ratio between two colors."""
            try:
                rgb1 = hex_to_rgb(color1)
                rgb2 = hex_to_rgb(color2)
                
                lum1 = relative_luminance(rgb1)
                lum2 = relative_luminance(rgb2)
                
                lighter = max(lum1, lum2)
                darker = min(lum1, lum2)
                
                return (lighter + 0.05) / (darker + 0.05)
            except:
                return 0.0
        
        # Analyze key contrast pairs
        contrasts = {
            'text_on_background': contrast_ratio(theme.text_primary, theme.background),
            'text_on_surface': contrast_ratio(theme.text_primary, theme.surface),
            'text_on_primary': contrast_ratio(theme.text_on_primary, theme.primary),
            'secondary_text_background': contrast_ratio(theme.text_secondary, theme.background),
            'success_background': contrast_ratio(theme.success, theme.background),
            'error_background': contrast_ratio(theme.error, theme.background),
            'warning_background': contrast_ratio(theme.warning, theme.background),
            'running_process_background': contrast_ratio(theme.process_running, theme.background),
            'waiting_process_background': contrast_ratio(theme.process_waiting, theme.background),
            'resource_background': contrast_ratio(theme.resource_available, theme.background)
        }
        
        return contrasts
    
    def get_accessibility_report(self, theme_name: str) -> Dict[str, Union[str, float, bool]]:
        """
        Generate a comprehensive accessibility report for a theme.
        
        Args:
            theme_name: Name of theme to analyze
            
        Returns:
            Dictionary containing accessibility analysis
        """
        if theme_name not in self.themes:
            return {}
        
        contrasts = self.analyze_contrast(theme_name)
        metadata = self.metadata.get(theme_name, None)
        
        # WCAG standards
        aa_normal = 4.5  # AA standard for normal text
        aa_large = 3.0   # AA standard for large text
        aaa_normal = 7.0 # AAA standard for normal text
        aaa_large = 4.5  # AAA standard for large text
        
        # Check compliance
        wcag_aa_compliant = all(ratio >= aa_normal for ratio in contrasts.values())
        wcag_aaa_compliant = all(ratio >= aaa_normal for ratio in contrasts.values())
        
        # Count passing ratios
        aa_passing = sum(1 for ratio in contrasts.values() if ratio >= aa_normal)
        aaa_passing = sum(1 for ratio in contrasts.values() if ratio >= aaa_normal)
        total_checks = len(contrasts)
        
        report = {
            'theme_name': theme_name,
            'wcag_aa_compliant': wcag_aa_compliant,
            'wcag_aaa_compliant': wcag_aaa_compliant,
            'aa_compliance_percentage': (aa_passing / total_checks) * 100 if total_checks > 0 else 0,
            'aaa_compliance_percentage': (aaa_passing / total_checks) * 100 if total_checks > 0 else 0,
            'contrast_ratios': contrasts,
            'colorblind_friendly': metadata.is_colorblind_friendly if metadata else False,
            'supports_dark_mode': metadata.supports_dark_mode if metadata else False,
            'accessibility_rating': metadata.accessibility_rating if metadata else 'Unknown',
            'recommendations': []
        }
        
        # Generate recommendations
        if not wcag_aa_compliant:
            report['recommendations'].append("Improve contrast ratios to meet WCAG AA standards (4.5:1)")
        
        for check_name, ratio in contrasts.items():
            if ratio < aa_normal:
                report['recommendations'].append(f"Improve contrast for {check_name} (current: {ratio:.2f}:1)")
        
        if not metadata or not metadata.is_colorblind_friendly:
            report['recommendations'].append("Consider colorblind accessibility")
        
        return report
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def generate_theme_preview(self, theme_name: str) -> Dict[str, str]:
        """
        Generate a preview representation of a theme.
        
        Args:
            theme_name: Name of theme to preview
            
        Returns:
            Dictionary with preview information
        """
        if theme_name not in self.themes:
            return {}
        
        theme = self.themes[theme_name]
        metadata = self.metadata.get(theme_name)
        
        preview = {
            'name': theme_name,
            'description': metadata.description if metadata else "Custom theme",
            'type': metadata.theme_type.value if metadata else "unknown",
            'process_colors': {
                'running': theme.process_running,
                'waiting': theme.process_waiting,
                'terminated': theme.process_terminated,
                'deadlocked': theme.process_deadlocked
            },
            'resource_colors': {
                'available': theme.resource_available,
                'allocated': theme.resource_allocated,
                'contested': theme.resource_contested
            },
            'background_colors': {
                'background': theme.background,
                'surface': theme.surface,
                'primary': theme.primary
            },
            'accessibility': {
                'rating': metadata.accessibility_rating if metadata else "Unknown",
                'colorblind_friendly': metadata.is_colorblind_friendly if metadata else False
            }
        }
        
        return preview
    
    def suggest_similar_themes(self, theme_name: str, count: int = 3) -> List[str]:
        """
        Suggest themes similar to the given theme.
        
        Args:
            theme_name: Name of reference theme
            count: Number of suggestions to return
            
        Returns:
            List of similar theme names
        """
        if theme_name not in self.themes:
            return []
        
        reference_meta = self.metadata.get(theme_name)
        if not reference_meta:
            return []
        
        # Score themes by similarity
        similarities = []
        
        for name, meta in self.metadata.items():
            if name == theme_name:
                continue
            
            score = 0
            
            # Same type bonus
            if meta.theme_type == reference_meta.theme_type:
                score += 3
            
            # Shared tags bonus
            shared_tags = set(meta.tags) & set(reference_meta.tags)
            score += len(shared_tags)
            
            # Accessibility similarity
            if meta.accessibility_rating == reference_meta.accessibility_rating:
                score += 2
            
            if meta.is_colorblind_friendly == reference_meta.is_colorblind_friendly:
                score += 1
            
            if meta.supports_dark_mode == reference_meta.supports_dark_mode:
                score += 1
            
            similarities.append((name, score))
        
        # Sort by similarity score and return top suggestions
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [name for name, score in similarities[:count]]
    
    def get_theme_statistics(self) -> Dict[str, Union[int, float, List[str]]]:
        """Get statistics about all available themes."""
        total_themes = len(self.themes)
        
        # Count by type
        type_counts = {}
        for meta in self.metadata.values():
            theme_type = meta.theme_type.value
            type_counts[theme_type] = type_counts.get(theme_type, 0) + 1
        
        # Accessibility stats
        accessible_themes = len(self.get_accessible_themes("AA"))
        colorblind_themes = len(self.get_colorblind_friendly_themes())
        dark_themes = len([m for m in self.metadata.values() if m.supports_dark_mode])
        
        # Most common tags
        all_tags = []
        for meta in self.metadata.values():
            all_tags.extend(meta.tags)
        
        tag_counts = {}
        for tag in all_tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        most_common_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'total_themes': total_themes,
            'themes_by_type': type_counts,
            'accessible_themes_count': accessible_themes,
            'colorblind_friendly_count': colorblind_themes,
            'dark_mode_count': dark_themes,
            'accessibility_percentage': (accessible_themes / total_themes) * 100 if total_themes > 0 else 0,
            'colorblind_percentage': (colorblind_themes / total_themes) * 100 if total_themes > 0 else 0,
            'most_common_tags': [tag for tag, count in most_common_tags],
            'all_theme_names': list(self.themes.keys())
        }

# =============================================================================
# BACKWARD COMPATIBILITY LAYER
# =============================================================================

# Create global instance for backward compatibility
_theme_manager = ColorThemes()

# Legacy class for backward compatibility
class ColorThemes:
    """
    Legacy class providing backward compatibility with the simple theme format.
    
    This maintains the original API while providing access to the enhanced theming system.
    """
    
    @property
    def DEFAULT(self) -> Dict[str, str]:
        """Get default theme as dictionary."""
        return _theme_manager.get_theme_dict("default") or {}
    
    @property 
    def DARK(self) -> Dict[str, str]:
        """Get dark theme as dictionary."""
        return _theme_manager.get_theme_dict("dark") or {}
    
    @property
    def COLORBLIND(self) -> Dict[str, str]:
        """Get colorblind theme as dictionary."""
        return _theme_manager.get_theme_dict("colorblind") or {}
    
    @classmethod
    def get_theme(cls, name: str) -> Dict[str, str]:
        """Get any theme by name as dictionary."""
        return _theme_manager.get_theme_dict(name) or {}
    
    @classmethod
    def list_themes(cls) -> List[str]:
        """List all available themes."""
        return _theme_manager.list_themes()
    
    @classmethod
    def get_manager(cls) -> ColorThemes:
        """Get the full theme manager for advanced features."""
        return _theme_manager

# =============================================================================
# FACTORY FUNCTIONS AND UTILITIES
# =============================================================================

def get_theme_manager() -> ColorThemes:
    """Get the global theme manager instance."""
    return _theme_manager

def get_theme(name: str) -> Optional[Dict[str, str]]:
    """
    Get a theme by name (convenience function).
    
    Args:
        name: Theme name
        
    Returns:
        Theme dictionary or None
    """
    return _theme_manager.get_theme_dict(name)

def list_available_themes() -> List[str]:
    """Get list of all available theme names."""
    return _theme_manager.list_themes()

def create_theme_from_colors(name: str, **colors) -> bool:
    """
    Create a simple custom theme from individual colors.
    
    Args:
        name: Name for the new theme
        **colors: Color values as keyword arguments
        
    Returns:
        bool: True if theme was created successfully
    """
    return _theme_manager.create_custom_theme(name, modifications=colors)

def get_accessible_themes(min_rating: str = "AA") -> List[str]:
    """Get themes meeting accessibility standards."""
    return _theme_manager.get_accessible_themes(min_rating)

def analyze_theme_accessibility(theme_name: str) -> Dict:
    """Analyze accessibility of a theme."""
    return _theme_manager.get_accessibility_report(theme_name)

# =============================================================================
# THEME PRESETS FOR SPECIFIC USE CASES
# =============================================================================

PRESET_MODIFICATIONS = {
    'presentation_light': {
        'background': '#ffffff',
        'text_primary': '#000000',
        'process_running': '#28a745',
        'process_waiting': '#dc3545'
    },
    'presentation_dark': {
        'background': '#1a1a1a',
        'text_primary': '#ffffff',
        'process_running': '#00ff7f',
        'process_waiting': '#ff4500'
    },
    'print_friendly': {
        'background': '#ffffff',
        'process_running': '#000000',
        'process_waiting': '#666666',
        'process_terminated': '#999999',
        'edge_allocation': '#000000',
        'edge_request': '#333333'
    },
    'high_visibility': {
        'process_running': '#00ff00',
        'process_waiting': '#ff0000',
        'process_deadlocked': '#ff00ff',
        'highlight': '#ffff00'
    }
}

def create_preset_theme(preset_name: str, base_theme: str = "default") -> bool:
    """
    Create a theme from a preset configuration.
    
    Args:
        preset_name: Name of the preset to create
        base_theme: Base theme to modify
        
    Returns:
        bool: True if successful
    """
    if preset_name in PRESET_MODIFICATIONS:
        modifications = PRESET_MODIFICATIONS[preset_name]
        return _theme_manager.create_custom_theme(
            preset_name, 
            base_theme, 
            modifications
        )
    return False

# =============================================================================
# MODULE INITIALIZATION AND TESTING
# =============================================================================

def print_theme_summary():
    """Print a summary of available themes and features."""
    manager = get_theme_manager()
    stats = manager.get_theme_statistics()
    
    print("🎨 Enhanced Color Themes Module")
    print("=" * 50)
    print(f"Total themes available: {stats['total_themes']}")
    print(f"Accessible themes (AA+): {stats['accessible_themes_count']}")
    print(f"Colorblind-friendly: {stats['colorblind_friendly_count']}")
    print(f"Dark mode support: {stats['dark_mode_count']}")
    print()
    
    print("Available themes:")
    for theme_name in stats['all_theme_names']:
        meta = manager.get_theme_metadata(theme_name)
        if meta:
            accessibility = "♿" if meta.is_colorblind_friendly else ""
            dark_mode = "🌙" if meta.supports_dark_mode else ""
            rating = f"[{meta.accessibility_rating}]"
            print(f"  • {theme_name} {rating} {accessibility} {dark_mode}")
    
    print()
    print("Legend: ♿ = Colorblind-friendly, 🌙 = Dark mode support")
    print(f"Most popular tags: {', '.join(stats['most_common_tags'])}")

# Usage example and testing
if __name__ == "__main__":
    print_theme_summary()
    
    # Test theme creation
    manager = get_theme_manager()
    success = manager.create_custom_theme(
        "test_theme",
        base_theme="default",
        modifications={
            'process_running': '#ff6b6b',
            'process_waiting': '#4ecdc4',
            'background': '#f7f1e3'
        }
    )
    
    if success:
        print(f"\n✅ Created test theme successfully")
        
        # Test accessibility analysis
        report = manager.get_accessibility_report("test_theme")
        print(f"   Accessibility rating: {report['accessibility_rating']}")
        print(f"   WCAG AA compliant: {report['wcag_aa_compliant']}")
    
    print("\n🎨 Enhanced themes module loaded successfully!")