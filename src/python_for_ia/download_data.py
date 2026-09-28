"""Download example data saved in different formats."""

from pathlib import Path
import pooch

SUBDIR = "example_formats"


def example_czi(data_root: Path):
    """
    Download example CZI data.

    Parameters
    ----------
    data_root: Path
        The root folder where the data will be saved. The data will be saved in
        `data_root`/example_formats.

    Returns
    -------
    Path
        Path to the downloaded data.
    """

    public_url = "https://pub-2ac5a4b342a7472da9d44847263e1a56.r2.dev"
    fname = "s_3_t_1_c_3_z_5.czi"
    data_path = pooch.retrieve(
        url=public_url + f"/{fname}",
        known_hash="9f6a1a154385de9c5655f14df997d2d2460a7655714cc7248d11160331429c27",
        fname=fname,
        path=data_root / SUBDIR,
    )
    return data_path


def example_czi_2(data_root: Path):
    """
    Download example CZI data.

    Parameters
    ----------
    data_root: Path
        The root folder where the data will be saved. The data will be saved in
        `data_root`/example_formats.

    Returns
    -------
    Path
        Path to the downloaded data.
    """

    url = (
        "https://zenodo.org/records/10577621/files/Intestine_3color_RAC.czi?download=1"
    )
    fname = "Intestine_3color_RAC.czi"
    data_path = pooch.retrieve(
        url=url,
        known_hash="b40eaa77c32d6d51d6ed9f8c485bc16c959fa8850a12ba17ea21e996eab8ea0c",
        fname=fname,
        path=data_root / SUBDIR,
    )
    return data_path


def example_czi_3(data_root: Path):
    """
    Download example CZI data.

    Parameters
    ----------
    data_root: Path
        The root folder where the data will be saved. The data will be saved in
        `data_root`/example_formats.

    Returns
    -------
    Path
        Path to the downloaded data.
    """

    url = "https://zenodo.org/records/3737795/files/qDII-CLV3-PIN1-PI-E35-LD-SAM6-T5.czi?download=1"
    fname = "qDII-CLV3-PIN1-PI-E35-LD-SAM6-T5.czi"
    data_path = pooch.retrieve(
        url=url,
        known_hash="3485f96a922dd13a1cabd3f26442bbc57178a89ed5164eb8468d3a27aa8c4060",
        fname=fname,
        path=data_root / SUBDIR,
    )
    return data_path


def example_nd2_1(data_root: Path):
    """
    Download example nd2 data.

    Parameters
    ----------
    data_root: Path
        The root folder where the data will be saved. The data will be saved in
        `data_root`/example_formats.

    Returns
    -------
    Path
        Path to the downloaded data.
    """

    public_url = "https://pub-2ac5a4b342a7472da9d44847263e1a56.r2.dev"
    fname = "ND2_aryeh_but3_cont200-1.nd2"
    data_path = pooch.retrieve(
        url=public_url + f"/{fname}",
        known_hash="9f6a1a154385de9c5655f14df997d2d2460a7655714cc7248d11160331429c27",
        fname=fname,
        path=data_root / SUBDIR,
    )
    return data_path


def example_nd2_2(data_root: Path):
    """
    Download example nd2 data.

    Parameters
    ----------
    data_root: Path
        The root folder where the data will be saved. The data will be saved in
        `data_root`/example_formats.

    Returns
    -------
    Path
        Path to the downloaded data.
    """

    url = "https://zenodo.org/records/8325290/files/CRISPR_MET1.nd2?download=1"
    fname = "CRISPR_MET1.nd2"
    data_path = pooch.retrieve(
        url=url,
        known_hash=" 8fee68d000d53bb8e13dccd4c1edb86cf910710a872cbd17f4d2ea5af885d43a",
        fname=fname,
        path=data_root / SUBDIR,
    )
    return data_path


def example_lif_1(data_root: Path):
    """
    Download example lif data.

    Parameters
    ----------
    data_root: Path
        The root folder where the data will be saved. The data will be saved in
        `data_root`/example_formats.

    Returns
    -------
    Path
        Path to the downloaded data.
    """

    public_url = "https://pub-2ac5a4b342a7472da9d44847263e1a56.r2.dev"
    fname = "s_1_t_4_c_2_z_1.lif"
    data_path = pooch.retrieve(
        url=public_url + f"/{fname}",
        known_hash="97cea3e600476492e3224101d4929781f4ab4a26218c57e10b0fc1aaf5190ddba",
        fname=fname,
        path=data_root / SUBDIR,
    )
    return data_path


def example_lif_2(data_root: Path):
    """
    Download example lif data.

    Parameters
    ----------
    data_root: Path
        The root folder where the data will be saved. The data will be saved in
        `data_root`/example_formats.

    Returns
    -------
    Path
        Path to the downloaded data.
    """

    url = "https://zenodo.org/records/13752242/files/20230828_SlFLS2-GFP_Flag-Mp10_Flag-alone_Remorin-RFP-3-3-1x.lif?download=1"
    fname = "20230828_SlFLS2-GFP_Flag-Mp10_Flag-alone_Remorin-RFP-3-3-1x.lif"
    data_path = pooch.retrieve(
        url=url,
        known_hash="037f8cd18295413c8536cdfb0a79bad12f7c69f983c9e64979f8ea5e5c686d91",
        fname=fname,
        path=data_root / SUBDIR,
    )
    return data_path


def example_ome_zarr_url():
    """
    Get a URL to OME-Zarr data.

    Returns
    -------
    str
        OME zarr URL.
    """
    return "https://uk1s3.embassy.ebi.ac.uk/idr/zarr/v0.5/idr0062A/6001240_labels.zarr"
