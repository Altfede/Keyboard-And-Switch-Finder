"""Modello dati per Keycaps"""
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from enum import Enum


class KeycapMaterial(str, Enum):
    PBT = "pbt"
    ABS = "abs"
    PBT_DOUBLESHOT = "pbt_doubleshot"
    ABS_DOUBLESHOT = "abs_doubleshot"
    PBT_DYESUB = "pbt_dyesub"


class KeycapProfile(str, Enum):
    CHERRY = "cherry"
    OEM = "oem"
    XDA = "xda"
    DSA = "dsa"
    SA = "sa"
    KAT = "kat"
    MDA = "mda"
    MT3 = "mt3"
    CHERRY_LOW = "cherry_low"


class LegendingType(str, Enum):
    DOUBLESHOT = "doubleshot"
    DYESUB = "dyesub"
    REVERSE_DYESUB = "reverse_dyesub"
    PAD_PRINT = "pad_print"
    LASER = "laser"
    BLANK = "blank"


class AestheticStyle(str, Enum):
    MONO = "mono"
    RETRO_BEIGE = "retro_beige"
    MINIMAL = "minimal"
    PASTELLO = "pastello"
    VAPORWAVE = "vaporwave"
    CARBON = "carbon"
    MONOCHROME = "monochrome"
    MIAMI = "miami"
    BOTANICAL = "botanical"
    WOB = "wob"  # White on Black
    BOW = "bow"  # Black on White


class KeycapSet(BaseModel):
    """Modello completo di un set di keycaps"""

    # Identificazione
    id: str
    name: str
    brand: str

    # Materiale e costruzione
    material: KeycapMaterial
    wall_thickness: float = Field(ge=1.0, le=2.0, description="Spessore pareti in mm")
    surface_finish: str = "textured"  # textured, smooth, glossy

    # Profilo
    profile: KeycapProfile
    profile_height: str = "medium"  # low, medium, high

    # Legending
    legending: LegendingType
    legend_quality: float = Field(ge=1, le=5, description="Qualità stampa/incisione")
    legend_language: List[str] = ["EN"]
    legend_alignment: str = "centered"  # centered, top_left

    # Estetica
    style: List[AestheticStyle] = []
    color_scheme: str

    # Compatibilità layout
    mx_compatible: bool = True
    layout_support: List[str] = ["ANSI"]  # ANSI, ISO, ISO_IT
    bottom_row_6_25u: bool = True
    bottom_row_7u: bool = False
    iso_enter: bool = False

    # Coverage
    base_kit_keys: int = Field(ge=61, le=150)
    includes_f13: bool = False
    includes_1_75u_shift: bool = False
    includes_2u_backspace: bool = False
    includes_iso_kit: bool = False
    includes_numpad: bool = False
    includes_novelties: bool = False
    includes_40_percent: bool = False
    includes_ortho: bool = False

    # Caratteristiche sound
    sound_signature: str = "thock"  # thock, clack, muted
    shine_resistance: float = Field(ge=1, le=5, description="Resistenza allo shine")

    # Fit e compatibilità
    stem_fit: str = "medium"  # tight, medium, loose
    north_facing_compatible: bool = True

    # Disponibilità e pricing
    availability_region: List[str] = ["EU"]
    stock_status: str = "in_stock"
    price_base_kit: Optional[float] = None
    price_with_extras: Optional[float] = None

    # Metadati
    verified: bool = False
    last_updated: str
    notes: Optional[str] = None
    image_url: Optional[str] = None

    def to_feature_vector(self) -> Dict[str, float]:
        """Converte il set in vettore di caratteristiche normalizzato"""
        return {
            # Materiale (one-hot)
            "material_pbt": 1.0 if "pbt" in self.material.lower() else 0.0,
            "material_abs": 1.0 if "abs" in self.material.lower() else 0.0,
            "material_doubleshot": 1.0 if "doubleshot" in self.material.lower() else 0.0,
            "material_dyesub": 1.0 if "dyesub" in self.material.lower() else 0.0,

            # Spessore normalizzato
            "thickness_norm": (self.wall_thickness - 1.0) / 1.0,

            # Profilo (one-hot principali)
            "profile_cherry": 1.0 if self.profile == KeycapProfile.CHERRY else 0.0,
            "profile_oem": 1.0 if self.profile == KeycapProfile.OEM else 0.0,
            "profile_xda": 1.0 if self.profile == KeycapProfile.XDA else 0.0,
            "profile_sa": 1.0 if self.profile == KeycapProfile.SA else 0.0,
            "profile_mt3": 1.0 if self.profile == KeycapProfile.MT3 else 0.0,

            # Altezza
            "height_low": 1.0 if self.profile_height == "low" else 0.0,
            "height_high": 1.0 if self.profile_height == "high" else 0.0,

            # Legending
            "legend_doubleshot": 1.0 if self.legending == LegendingType.DOUBLESHOT else 0.0,
            "legend_quality_norm": self.legend_quality / 5.0,

            # Layout
            "layout_iso": 1.0 if "ISO" in self.layout_support else 0.0,
            "layout_iso_it": 1.0 if "ISO_IT" in self.layout_support else 0.0,
            "iso_enter": 1.0 if self.iso_enter else 0.0,

            # Coverage
            "coverage_complete": 1.0 if self.base_kit_keys >= 120 else 0.0,
            "includes_numpad": 1.0 if self.includes_numpad else 0.0,

            # Sound
            "sound_thock": 1.0 if self.sound_signature == "thock" else 0.0,
            "sound_clack": 1.0 if self.sound_signature == "clack" else 0.0,

            # Qualità
            "shine_resistance_norm": self.shine_resistance / 5.0,

            # Compatibilità
            "north_facing_safe": 1.0 if self.north_facing_compatible else 0.0,
        }

    class Config:
        use_enum_values = True
