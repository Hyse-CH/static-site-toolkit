import jinja2
import os
from pathlib import Path
from shutil import rmtree
import json

helpTxt = """Arguments:
    help - Gives commands usage
    build - build a project"""

def cmdHelp() -> None:
    print(helpTxt)

projectInfo = {}

def cmdBuild() -> None:
    projectPath: str = os.getcwd()

    # Detect if it's a project
    if not Path(f'{projectPath}/stk.json').is_file():
        print('Error: this directory isn\'t a STK project')
        return

    with open(f'{projectPath}/stk.json', 'r') as f:
        projectInfo = json.loads(f.read())

    # Declaring useful variables
    srcDir: str = f'{projectPath}/src'
    buildDir: str = f'{projectPath}/build'
    pageDir: str = '/pages'
    indexPath: str = '/index.jinja'
    dataDir: str = f'{srcDir}/data'
    componentsDir: str = '/components'
    headerPath: str = f'{componentsDir}/header.jinja'
    footerPath: str = f'{componentsDir}/footer.jinja'

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(srcDir))

    indexTemplate = env.get_template(indexPath)

    if Path(buildDir).is_dir():
        rmtree(buildDir)
                 
    os.mkdir(buildDir)
    

    header = env.get_template(headerPath).render()
    footer = env.get_template(footerPath).render()

    for file in os.listdir(f'{srcDir}/{pageDir}'):
        if not file.endswith('.jinja'):
            continue

        template = env.get_template(f'{pageDir}/{file}')
        
        newFileName: str

        # Checks if the file is the index
        if file == 'home.jinja':
            newFileName = 'index.html'
        else:
            newFileName = f'{file[:len(file) - 6]}.html'
        
        fileData = {}
        # print(f'{dataDir}/{newFileName[:len(newFileName) - 5]}.json')
        with open(f'{dataDir}/{file[:len(file) - 6]}.json', 'r') as f:
            fileData = json.loads(f.read())
        
        with open(f'{buildDir}/{newFileName}', 'w') as f:
            halfRenderedFile = template.render(data=fileData['data'])
            renderedFile = indexTemplate.render(
                header=header,
                content=halfRenderedFile,
                footer=footer, 
                name=projectInfo['name'],
                stylesheets=fileData['stylesheets'],
                rawHeadDatas=fileData['rawHeadDatas']
            )
            f.write(renderedFile)

