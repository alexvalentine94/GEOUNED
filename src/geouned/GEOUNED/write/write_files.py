from . import additional_files as OutFiles
from .mcnp_format import McnpInput
from .openmc_format import OpenmcInput
from .phits_format import PhitsInput
from .serpent_format import SerpentInput
import os


def write_geometry(
    UniverseBox,
    MetaList,
    Surfaces,
    settings,
    options,
    tolerances,
    numeric_format,
    geometryName,
    outFormat,
    cellCommentFile,
    cellSummaryFile,
    title,
    volSDEF,
    volCARD,
    UCARD,
    dummyMat,
    step_filename,
):

    supported_mc_codes = ("mcnp", "openmc_xml", "openmc_py", "serpent", "phits")
    for out_format in outFormat:
        if out_format not in supported_mc_codes:
            msg = f"outFormat {out_format} not in supported MC codes ({supported_mc_codes})"
            raise ValueError(msg)

    # write cells comments in file
    if cellCommentFile:
        OutFiles.comments_write(geometryName, MetaList)
    if cellSummaryFile:
        OutFiles.summary_write(geometryName, MetaList)

    if "mcnp" in outFormat:
        mcnpDir = os.path.join(os.getcwd(), 'mcnp')
        os.makedirs(mcnpDir, exist_ok=True)
        mcnpFilename = os.path.join(mcnpDir, geometryName + ".mcnp")
        outBox = (
            UniverseBox.XMin,
            UniverseBox.XMax,
            UniverseBox.YMin,
            UniverseBox.YMax,
            UniverseBox.ZMin,
            UniverseBox.ZMax,
        )
        if settings.voidGen:
            outSphere = (Surfaces["Sph"][-1].Index, Surfaces["Sph"][-1].Surf.Radius)
        else:
            outSphere = None

        MCNPfile = McnpInput(
            MetaList,
            Surfaces,
            options,
            tolerances,
            numeric_format,
            title,
            volSDEF,
            volCARD,
            UCARD,
            dummyMat,
            step_filename,
        )
        MCNPfile.set_sdef((outSphere, outBox))
        MCNPfile.write_input(mcnpFilename)

    if "openmc_xml" in outFormat or "openmc_py" in outFormat:
        OMCFile = OpenmcInput(MetaList, Surfaces, options, tolerances, numeric_format)

    if "openmc_xml" in outFormat:
        openmcDir = os.path.join(os.getcwd(), 'openmc_xml')
        os.makedirs(openmcDir, exist_ok=True)
        omcFilename = os.path.join(openmcDir, geometryName + ".xml")
        OMCFile.write_xml(omcFilename)

    if "openmc_py" in outFormat:
        openmcDir = os.path.join(os.getcwd(), 'openmc_py')
        os.makedirs(openmcDir, exist_ok=True)
        omcFilename = os.path.join(openmcDir, geometryName + ".py")
        OMCFile.write_py(omcFilename)

    if "serpent" in outFormat:
        outBox = (
            UniverseBox.XMin,
            UniverseBox.XMax,
            UniverseBox.YMin,
            UniverseBox.YMax,
            UniverseBox.ZMin,
            UniverseBox.ZMax,
        )
        if settings.voidGen:
            outSphere = (Surfaces["Sph"][-1].Index, Surfaces["Sph"][-1].Surf.Radius)
        else:
            outSphere = None

        Serpentfile = SerpentInput(
            MetaList,
            Surfaces,
            options,
            tolerances,
            numeric_format,
            title,
            volSDEF,
            volCARD,
            UCARD,
            dummyMat,
            step_filename,
        )
        # Serpentfile.set_sdef((outSphere,outBox))
        serpentDir = os.path.join(os.getcwd(), 'serpent')
        os.makedirs(serpentDir, exist_ok=True)
        serpentFilename = os.path.join(serpentDir, geometryName + ".serp")
        Serpentfile.write_input(serpentFilename)

    if "phits" in outFormat:
        PHITS_outBox = (
            UniverseBox.XMin,
            UniverseBox.XMax,
            UniverseBox.YMin,
            UniverseBox.YMax,
            UniverseBox.ZMin,
            UniverseBox.ZMax,
        )
        if settings.voidGen:
            PHITS_outSphere = (
                Surfaces["Sph"][-1].Index,
                Surfaces["Sph"][-1].Surf.Radius,
            )
        else:
            PHITS_outSphere = None

        PHITSfile = PhitsInput(
            MetaList,
            Surfaces,
            options,
            tolerances,
            numeric_format,
            title,
            volSDEF,
            volCARD,
            UCARD,
            dummyMat,
            step_filename,
            matFile=settings.matFile,
            voidMat=settings.voidMat,
            startCell=settings.startCell,
        )
        # PHITSfile.setSDEF_PHITS((PHITS_outSphere,PHITS_outBox))
        phitsDir = os.path.join(os.getcwd(), 'phits')
        os.makedirs(phitsDir, exist_ok=True)
        phitsFilename = os.path.join(phitsDir, geometryName + ".phits")
        PHITSfile.write_phits(phitsFilename)
