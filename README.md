# MagicLeap Omniverse In Scene UI Tutorial Extension

Full code sample from the tutorial available on the MagicLeap Developer Portal here-
https://developer-docs.magicleap.cloud/docs/guides/remote-rendering/Applications/Omniverse/in-scene-ui-tutorial/

based on the *Omniverse Kit* Extensions Project Template-
https://github.com/NVIDIA-Omniverse/kit-extension-template

Getting started & plugin installation documentation from the template project-

# Getting Started

## Install Omniverse and some Apps

1. Install *Omniverse Launcher*: [download](https://www.nvidia.com/en-us/omniverse/download)
2. Install and launch one of *Omniverse* apps in the Launcher. For instance: *Code*.

## Add a new extension to your *Omniverse App*

1. Fork and clone this repo, for example in `C:\projects\kit-extension-template`
2. In the *Omniverse App* open extension manager: *Window* &rarr; *Extensions*.
3. In the *Extension Manager Window* open a settings page, with a small gear button in the top left bar.
4. In the settings page there is a list of *Extension Search Paths*. Add cloned repo `exts` subfolder there as another search path: `C:\projects\kit-extension-template\exts`

![Extension Manager Window](/images/add-ext-search-path.png)

5. Now you can find `omni.hello.world` extension in the top left search bar. Select and enable it.
6. "My Window" window will pop up. *Extension Manager* watches for any file changes. You can try changing some code in this extension and see them applied immediately with a hotreload.

### Few tips

* Now that `exts` folder was added to the search you can add new extensions to this folder and they will be automatically found by the *App*.
* Look at the *Console* window for warnings and errors. It also has a small button to open current log file.
* All the same commands work on linux. Replace `.bat` with `.sh` and `\` with `/`.
* Extension name is a folder name in `exts` folder, in this example: `omni.hello.world`. 
* Most important thing extension has is a config file: `extension.toml`, take a peek.

## Next Steps: Alternative way to add a new extension

To get a better understanding and learn a few other things, we recommend following next steps:

1. Remove search path added in the previous section.
1. Open this cloned repo using Visual Studio Code: `code C:\projects\kit-extension-template`. It will suggest installing a few extensions to improve python experience.
2. In the terminal (CTRL + \`) run `link_app.bat` (more in [Linking with an *Omniverse* app](#linking-with-an-omniverse-app) section).
3. Run this app with `exts` folder added as an extensions search path and new extension enabled:

```bash
> app\omni.code.bat --ext-folder exts --enable omni.hello.world
```

- `--ext-folder [path]` - adds new folder to the search path
- `--enable [extension]` - enables an extension on startup.

Use `-h` for help:

```bash
> app\omni.code.bat -h
```

4. After the *App* started you should see:
    * new "My Window" window popup.
    * extension search paths in *Extensions* window as in the previous section.
    * extension enabled in the list of extensions.

5. If you look inside `omni.code.bat` or any other *Omniverse App*, they all run *Omniverse Kit* (`kit.exe`). *Omniverse Kit* is the Omniverse Application runtime that powers *Apps* build out of extensions.
Think of it as `python.exe`. It is a small runtime, that enables all the basics, like settings, python, logging and searches for extensions. **Everything else is an extension.** You can run only this new extension without running any big *App* like *Code*:


```bash
> app\kit\kit.exe --ext-folder exts --enable omni.hello.world
```

It starts much faster and will only have extensions enabled that are required for this new extension (look at  `[dependencies]` section of `extension.toml`). You can enable more extensions: try adding `--enable omni.kit.window.extensions` to have extensions window enabled (yes, extension window is an extension too!):


```bash
> app\kit\kit.exe --ext-folder exts --enable omni.hello.world --enable omni.kit.window.extensions
```

You should see a menu in the top left. From here you can enable more extensions from the UI. 

### Few tips

* In the *Extensions* window, press *Bread* button near the search bar and select *Show Extension Graph*. It will show how the current *App* comes to be: all extensions and dependencies.
* Extensions system documentation: http://omniverse-docs.s3-website-us-east-1.amazonaws.com/kit-sdk/104.0/docs/guide/extensions.html


# Linking with an *Omniverse* app

For a better developer experience, it is recommended to create a folder link named `app` to the *Omniverse Kit* app installed from *Omniverse Launcher*. A convenience script to use is included.

Run:

```bash
> link_app.bat
```

If successful you should see `app` folder link in the root of this repo.

If multiple Omniverse apps is installed script will select recommended one. Or you can explicitly pass an app:

```bash
> link_app.bat --app create
```

You can also just pass a path to create link to:

```bash
> link_app.bat --path "C:/Users/bob/AppData/Local/ov/pkg/create-2021.3.4"
```

# Adding a new extension

Adding a new extension is as simple as copying and renaming existing one:

1. copy `exts/omni.hello.world` to `exts/[new extension name]`
2. rename python module (namespace) in `exts/[new extension name]/omni/hello/world` to `exts/[new extension name]/[new python module]`
3. update `exts/[new extension name]/config/extension.toml`, most importantly specify new python module to load:

```toml
[[python.module]]
name = "[new python module]"
```

No restart is needed, you should be able to find and enable `[new extension name]` in extension manager.

# Sharing extensions

To make extension available to other users use [Github Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

1. Make sure the repo has [omniverse-kit-extension](https://github.com/topics/omniverse-kit-extension) topic set for auto discovery.
2. For each new release increment extension version (in `extension.toml`) and update the changelog (in `docs/CHANGELOG.md`). [Semantic versionning](https://semver.org/) must be used to express severity of API changes.

# Contributing
The source code for this repository is provided as-is and we are not accepting outside contributions.