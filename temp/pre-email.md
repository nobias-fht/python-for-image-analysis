Hi!

The python for image analysis course starts next week!

Here are instructions to ensure everyone has the required software before the course starts, please make sure the following tools are installed on the machine that you will use for the course:

- **Git** — for downloading and working with the course repository.
- **`uv`** — the Python package and environment manager we will use throughout the course.
- **Visual Studio Code (VS Code)** — the editor we will use.

Find instructions to download each tool below.
If you are having any issues with the installation please do not hesitate to get in contact.

## Visual Studio Code and extensions

Visual Studio Code is available for install from the ***Company Portal*** app for **Windows** and the ***HT Self Service*** app for **Mac**.
Search for "Visual Studio Code" and install if you do not have it already.

Once VS Code is installed, we need to install some extensions:

1. Open the application

2. Navigate to the extensions tab in the side bar.

    ![VSCode extensions icon](extensions.png)

3. Search for and install the ***Python*** extension and the ***Jupyter*** extension.
![Python VSCode extension](python_extension.png)
![Jupyter VSCode extension](jupyter_extension.png)

## `uv`

1. Check if `uv` in already installed with:

    ```
    uv --version
    ```
    if this prints a version number `uv` is already installed.

2. Install `uv`:

    Instructions to install `uv` for **Windows** and **Mac** are available here: https://docs.astral.sh/uv/getting-started/installation.

    There are many installation options: for **Windows** we can use `irm` with `iex`, or it is available via `winget`; for **Mac** we can use `curl`, `wget` or `brew`.



## Git

1. Check if Git is already installed with:

    ```console
    git --version
    ```

    If you see a version number, Git is already installed.

    If not you will need to install Git.

2. Instructions for installation for **Windows** and **Mac** are summarized from https://git-scm.com/install/.

    i. Install Git on **Windows**:

    You can install *Git for Windows* from: https://gitforwindows.org/.

    Alternatively you can use `winget`.

    ```
    winget install --id Git.Git -e --source winget
    ```

    ii. Install Git on **Mac**:

    One option is to install Apple's developer [command line tools](https://developer.apple.com/documentation/xcode/installing-the-command-line-tools#Install-the-Command-Line-Tools-package-in-Terminal), which includes Git. This can be triggered with the following command.

    ```
    xcode-select --install
    ```





    
