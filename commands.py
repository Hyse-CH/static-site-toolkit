import jinja2
import os
from pathlib import Path
from shutil import rmtree

helpTxt = """Arguments:
    help - Gives commands usage
    build - build a project"""

def cmdHelp() -> None:
    print(helpTxt)

def cmdBuild() -> None:
    projectPath: str = os.getcwd()

    # Detect if it's a project
    if not Path(f'{projectPath}/stk.json').is_file():
        print('Error: this directory isn\'t a STK project')
        return

    # Declaring useful variables
    srcDir: str = f'{projectPath}/src'
    buildDir: str = f'{projectPath}/build'
    pageDir: str = '/pages'
    indexPath: str = f'/index.jinja'
    componentsDir: str = f'/components'
    headerPath = f'{componentsDir}/header.jinja'
    footerPath = f'{componentsDir}/footer.jinja'

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(srcDir))

    indexTemplate = env.get_template(indexPath)


    if Path(buildDir).is_dir():
        rmtree(buildDir)
                 
    os.mkdir(buildDir)
    

    header = env.get_template(headerPath).render()
    footer = env.get_template(footerPath).render()

    print(pageDir)

    for file in os.listdir(f'{srcDir}/{pageDir}'):
        if not file.endswith('.jinja'):
            continue

        template = env.get_template(f'{pageDir}/{file}')
        
        print(f'{pageDir}/{file}')

        newFileName: str

        if file == 'home.jinja':
            newFileName = 'index.html'
        else:
            newFileName = file[:len(file) - 6]
        
        with open(f'{buildDir}/{newFileName}', 'w') as f:
            halfRenderedFile = template.render()
            renderedFile = indexTemplate.render(header=header, content=halfRenderedFile, footer=footer)
            f.write(renderedFile)

