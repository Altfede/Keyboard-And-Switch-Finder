"""Modello dati per Tastiere complete"""
from typing import Optional, List, Dict
from pydantic import BaseModel, Field
from enum import Enum


class FormFactor(str, Enum):
    FULL_SIZE = "100%"
    NINETY_SIX = "96%"
    NINETY_EIGHT = "98%"
    TKL = "80%"
    SEVENTY_FIVE = "75%"
    SIXTY_FIVE = "65%"
    SIXTY = "60%"
    FORTY = "40%"


class MountingType(str, Enum):
    TRAY = "tray"
    TOP = "top"
    GASKET = "gasket"
    LEAF_SPRING = "leaf_spring"
    O_RING = "o_ring"
    PLATELESS = "plateless"


class CaseMaterial(str, Enum):
    ALUMINUM = "aluminum"
    POLYCARBONATE = "polycarbonate"
    ABS = "abs"
    ACRYLIC = "acrylic"
    WOOD = "wood"
    HYBRID = "hybrid"


class PlateMaterial(str, Enum):
    POLYCARBONATE = "polycarbonate"
    POM = "pom"
    FR4 = "fr4"
    ALUMINUM = "aluminum"
    BRASS = "brass"
    STEEL = "steel"


class StabilizerType(str, Enum):
    PLATE_MOUNT = "plate_mount"
    SCREW_IN = "screw_in"
    SNAP_IN = "snap_in"


class Connectivity(str, Enum):
    WIRED = "wired"
    WIRELESS_24 = "wireless_2.4"
    BLUETOOTH = "bluetooth"
    BLUETOOTH_MULTIPOINT = "bluetooth_multipoint"
    HYBRID = "hybrid"


class Board(BaseModel):
    """Modello completo di una tastiera meccanica"""

    # Identificazione
    id: str
    name: str
    brand: str

    # Form factor e layout
    form_factor: FormFactor
    layout: List[str] = ["ANSI"]  # ANSI, ISO, ISO_IT
    has_numpad: bool = True
    has_function_row: bool = True
    has_arrow_keys: bool = True

    # Architettura
    hot_swap: bool = False
    hot_swap_pin_support: Optional[int] = None  # 3 o 5
    pcb_orientation: str = "south_facing"  # south_facing, north_facing

    # Mounting e costruzione
    mounting_type: MountingType
    case_material: CaseMaterial
    plate_material: Optional[PlateMaterial] = None
    plate_options: List[PlateMaterial] = []

    # Stabilizzatori
    stabilizer_type: StabilizerType
    factory_lubed_stabs: bool = False

    # Foam e dampening
    case_foam: bool = False
    plate_foam: bool = False
    pcb_foam: bool = False

    # Connettività
    connectivity: List[Connectivity] = [Connectivity.WIRED]
    latency_ms: Optional[float] = None
    battery_mah: Optional[int] = None
    battery_life_hours: Optional[int] = None

    # Software e programmabilità
    software: List[str] = []  # QMK, VIA, Vial, proprietary
    macro_layers: int = 0
    programmable: bool = False

    # RGB e illuminazione
    rgb_per_key: bool = False
    rgb_single_zone: bool = False
    rgb_underglow: bool = False

    # Features extra
    has_knob: bool = False
    has_media_keys: bool = False
    nkro: bool = True

    # Sound characteristics
    sound_signature: List[str] = []  # thock, clack, muted, marbly

    # Caratteristiche fisiche
    weight_grams: Optional[int] = None
    dimensions_mm: Optional[Dict[str, float]] = None  # length, width, height

    # Tipo prodotto
    product_type: str = "prebuilt"  # prebuilt, barebone, kit

    # Prebuilt specifics
    included_switches: Optional[str] = None
    included_keycaps: Optional[str] = None

    # Disponibilità e pricing
    availability_region: List[str] = ["EU"]
    stock_status: str = "in_stock"
    price: Optional[float] = None
    price_barebone: Optional[float] = None

    # Metadati
    verified: bool = False
    last_updated: str
    notes: Optional[str] = None
    image_url: Optional[str] = None

    def to_feature_vector(self) -> Dict[str, float]:
        """Converte la board in vettore di caratteristiche normalizzato"""
        return {
            # Form factor (one-hot)
            "ff_full": 1.0 if self.form_factor == FormFactor.FULL_SIZE else 0.0,
            "ff_tkl": 1.0 if self.form_factor == FormFactor.TKL else 0.0,
            "ff_75": 1.0 if self.form_factor == FormFactor.SEVENTY_FIVE else 0.0,
            "ff_65": 1.0 if self.form_factor == FormFactor.SIXTY_FIVE else 0.0,
            "ff_60": 1.0 if self.form_factor == FormFactor.SIXTY else 0.0,

            # Layout
            "layout_iso": 1.0 if "ISO" in self.layout else 0.0,
            "layout_iso_it": 1.0 if "ISO_IT" in self.layout else 0.0,

            # Features strutturali
            "has_numpad": 1.0 if self.has_numpad else 0.0,
            "has_arrows": 1.0 if self.has_arrow_keys else 0.0,
            "has_f_row": 1.0 if self.has_function_row else 0.0,

            # Hot-swap
            "hot_swap": 1.0 if self.hot_swap else 0.0,
            "hot_swap_5pin": 1.0 if self.hot_swap_pin_support == 5 else 0.0,

            # PCB orientation
            "south_facing": 1.0 if self.pcb_orientation == "south_facing" else 0.0,

            # Mounting (one-hot)
            "mount_gasket": 1.0 if self.mounting_type == MountingType.GASKET else 0.0,
            "mount_tray": 1.0 if self.mounting_type == MountingType.TRAY else 0.0,
            "mount_top": 1.0 if self.mounting_type == MountingType.TOP else 0.0,

            # Case material (one-hot)
            "case_aluminum": 1.0 if self.case_material == CaseMaterial.ALUMINUM else 0.0,
            "case_pc": 1.0 if self.case_material == CaseMaterial.POLYCARBONATE else 0.0,

            # Plate material (one-hot se presente)
            "plate_pc": 1.0 if self.plate_material == PlateMaterial.POLYCARBONATE else 0.0,
            "plate_aluminum": 1.0 if self.plate_material == PlateMaterial.ALUMINUM else 0.0,
            "plate_brass": 1.0 if self.plate_material == PlateMaterial.BRASS else 0.0,

            # Stabilizzatori
            "stabs_screw_in": 1.0 if self.stabilizer_type == StabilizerType.SCREW_IN else 0.0,
            "stabs_lubed": 1.0 if self.factory_lubed_stabs else 0.0,

            # Foam
            "has_foam": 1.0 if (self.case_foam or self.plate_foam or self.pcb_foam) else 0.0,

            # Connettività
            "wireless": 1.0 if any("bluetooth" in c or "wireless" in c for c in self.connectivity) else 0.0,
            "wired": 1.0 if Connectivity.WIRED in self.connectivity else 0.0,

            # Latenza normalizzata (se presente, <5ms ottimo, >20ms problematico)
            "low_latency": 1.0 if (self.latency_ms and self.latency_ms < 5) else 0.5,

            # Software
            "qmk_via": 1.0 if any("QMK" in s or "VIA" in s for s in self.software) else 0.0,
            "programmable": 1.0 if self.programmable else 0.0,

            # RGB
            "rgb_per_key": 1.0 if self.rgb_per_key else 0.0,

            # Features
            "has_knob": 1.0 if self.has_knob else 0.0,
            "nkro": 1.0 if self.nkro else 0.0,

            # Sound signature
            "sound_thock": 1.0 if "thock" in self.sound_signature else 0.0,
            "sound_clack": 1.0 if "clack" in self.sound_signature else 0.0,
            "sound_muted": 1.0 if "muted" in self.sound_signature else 0.0,

            # Peso normalizzato (500g-2000g -> 0-1, leggero vs pesante)
            "weight_norm": (self.weight_grams - 500) / 1500 if self.weight_grams else 0.5,

            # Tipo prodotto
            "prebuilt": 1.0 if self.product_type == "prebuilt" else 0.0,
            "barebone": 1.0 if self.product_type == "barebone" else 0.0,
        }

    def estimate_noise_score(self, switch_type: Optional[str] = None) -> float:
        """
        Stima il noise score 1-5 (1=silenzioso, 5=rumoroso)
        basato su mounting, foam, case material e switch
        """
        base_noise = 3.0

        # Mounting impact
        if self.mounting_type == MountingType.GASKET:
            base_noise -= 0.5
        elif self.mounting_type == MountingType.TRAY:
            base_noise += 0.5

        # Foam dampening
        if self.case_foam:
            base_noise -= 0.3
        if self.plate_foam:
            base_noise -= 0.2

        # Case material
        if self.case_material == CaseMaterial.ALUMINUM:
            base_noise += 0.3
        elif self.case_material == CaseMaterial.POLYCARBONATE:
            base_noise -= 0.2

        # Switch type impact (se fornito)
        if switch_type:
            if "silent" in switch_type.lower():
                base_noise -= 1.0
            elif "clicky" in switch_type.lower():
                base_noise += 1.0

        return max(1.0, min(5.0, base_noise))

    class Config:
        use_enum_values = True
