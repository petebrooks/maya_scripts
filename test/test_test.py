import core

def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 4

def test_toMaterialName():
  assert core.namedMaterial.toMaterialName("cockatoo_Geo") == "cockatoo_Mat"
  assert core.namedMaterial.toMaterialName("cockatoo_Geo_lo") == "cockatoo_Mat"
  assert core.namedMaterial.toMaterialName("cockatoo_Geo_s_lo") == "cockatoo_Mat"
  assert core.namedMaterial.toMaterialName("cockatoo_Geo_2") == "cockatoo_Mat"
  assert core.namedMaterial.toMaterialName("cockatoo_Geo_2_lo") == "cockatoo_Mat"
