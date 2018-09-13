# xadmin-svgimagefield-plugin

## Environ
Python 2.7 

django==1.9.9

xadmin@master

## Usage:

In your admix file

```
from xplugin_svgimagefield import SVGAndImagePlugin


site.register_plugin(SVGAndImagePlugin, ModelFormAdminView)
```
With this, the fields in the edit form will support the svg format (as well as the formats already supported).

`has_svgimagefield = False`  Allows to disable the form's plugin.

`exclude_svgimagefield = ()`  Excludes changes in the plugin configured fields.