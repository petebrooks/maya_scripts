- get shape node given transform
- find by name, returns first match or None
- mesh basename
```
def mesh_basename(mesh):
  re.match(r"(.+)_(?:Geo|(?:s_)?lo).*", str(mesh)).group(1)
```
- file dialogs
