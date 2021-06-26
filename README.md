![image](./buildozer/data/github_image.png)

An android piano app made in Kivy(python)

Visit [Releases](/releases) to download .apk

## Table of contents:
- [General Info](#General-Info)
- [Screenshots](#Screenshots)
- [Tools Used](#Tools-Used)
- [Contributing](#Contributing)

## General Info

This was an app made just to learn kivy. There may be releases of this app (Or not)
Secondly, the apk's are so big because wav files for audio were used. Those are not used by choice, rather only wav files were able to play on android after deployment (because of p4android, kivy works great with mp3).

## Screenshots

## Tools Used

- Python 3.8
- [Kivy 2.0.0](https://github.com/kivy/kivy)
- [KivyMD 0.104.2](https://github.com/kivymd/KivyMD)
- [Buildozer](https://github.com/kivy/buildozer) (Buildozer uses SDK,NDK,Gradle and other tools)

## Contributing

### Setting up environment

**Install Kivy**


Install Kivy dependencies (using apt)
    
    sudo apt-get install -y python-pip build-essential git python python-dev libav-tools ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev

Install Kivy dependencies (using pip)

    pip install cython
    
Install Kivy
    
    pip install git+https://github.com/kivy/kivy.git@master

**Install KivyMD**

    pip install https://github.com/kivymd/KivyMD/archive/master.zip
    
**Install Buildozer**

    pip install --user https://github.com/kivy/buildozer/archive/master.zip

### Build using Buildozer

Install dependencies (mentioned for only **Debian/Ubuntu**)

    sudo apt install make cmake lld libssl-dev libtool autoconf default-jdk

Clone [this](.) repository
            
    git clone https://github.com/RaviRahar/Piano.git

Change to 'Piano' directory
            
    cd Piano/buildozer

Build apk with
    
    buildozer android debug 
    
**NOTE:** 
- before last step use `export GRADLE_OPTS="-Xms1724m -Xmx5048m -Dorg.gradle.jvmargs='-Xms1724m -Xmx5048m'"` if having build fails saying `Execution failed for task ':packageDebug'.`
- use the specified buildozer.spec file only
- if icons don't get displayed, then buildozer did not install the last mentioned requirement from `buildozer.spec` . Happend with me, add any random library or add name of a library twice, one being at the end of list. (for eg: add kivy==2.0.0 in `buildozer.spec` at the end of the line saying `requirements: `)
  
