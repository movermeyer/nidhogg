import sys
import os
cwd = os.getcwd()
project_root = os.path.dirname(cwd)
sys.path.insert(0, project_root)
import nidhogg
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.viewcode']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'Open-source Minecraft server bootstrapping platform'
copyright = u'2014, Andriy Kushnir (Orhideous)'
version = nidhogg.__version__
release = nidhogg.__version__
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = 'nature'
html_static_path = ['_static']
htmlhelp_basename = 'lsapidoc'
