"""Static/near-static reference data for the StudySetup/StudyBuilder forms: which system
types and machine variants exist, and the picklists behind the metocean sources that need
one (DNV Weibull zones, Copernicus products, NDBC buoys -- "hindcast_upload" doesn't, since
the file itself carries no location). None of them depend on a particular study, so they're
plain unparameterized GETs rather than living under /api/studies/{id}/..., and the frontend
fetches each one once per page load (see api.ts's `once`)."""

from fastapi import APIRouter

from .. import pybm_service
from ..weibull_locations import LOCATIONS

router = APIRouter(prefix="/api", tags=["machines"])


@router.get("/machines")
def get_machines():
    """The fixed set of machine variants PyBM ships (see pybm_service.MACHINE_TYPES) --
    populates the "System" dropdown in StudyBuilder.tsx (filtered client-side to the
    study's own system_type)."""
    return {"machines": pybm_service.machine_type_list()}


@router.get("/system-types")
def get_system_types():
    """The 3 system types a study can be fixed to once, at Study Setup -- populates
    StudySetup.tsx's system-type picker."""
    return {"system_types": pybm_service.system_type_list()}


@router.get("/locations")
def get_locations():
    """The 104 DNV-RP-C205 nautic zones. See weibull_locations.py for where LOCATIONS
    itself comes from."""
    return {
        "locations": [
            {"id": loc_id, "label": entry["label"], "zone": entry["zone"], "bbox": entry["bbox"]}
            for loc_id, entry in LOCATIONS.items()
        ]
    }


@router.get("/copernicus-products")
def get_copernicus_products():
    """The handful of Copernicus Marine reanalysis products PyBM's CopernicusLoader
    supports -- populates the "Product / region" dropdown once Copernicus is picked as the
    scatter source; see pybm_service.COPERNICUS_PRODUCTS for the actual list."""
    return {"products": pybm_service.COPERNICUS_PRODUCTS}


@router.get("/ndbc-buoys")
def get_ndbc_buoys():
    """Real NOAA buoys with a confirmed historical wave record -- backs the map picker in
    NdbcBuoyPickerModal.tsx. The filtering (and its slow first call) all happens in
    pybm_service.list_ndbc_buoys(), not here."""
    return {"buoys": pybm_service.list_ndbc_buoys()}
