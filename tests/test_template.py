import os
import sys
from datetime import datetime
import gc

pkg_dir = os.path.join(os.path.dirname(__file__),'..')
sys.path.append(pkg_dir)

# from refcount.interop import *
# from refcount.putils import library_short_filename

# fname = library_short_filename("test_native_library")

# if(sys.platform == 'win32'):
#     dir_path = os.path.join(pkg_dir, 'tests/test_native_library/x64/Debug')
# else:
#     dir_path = os.path.join(pkg_dir, 'tests/test_native_library/build')

# native_lib_path = os.path.join(dir_path, fname)

# assert os.path.exists(native_lib_path)

# def test_native_obj_ref_counting():
#     dog = Dog()
#     assert 1 == dog.reference_count
#     assert 1 == dog.native_reference_count
#     dog.add_ref()
#     assert 2 == dog.reference_count
#     assert 1 == dog.native_reference_count
#     owner = DogOwner(dog)
#     assert 1 == owner.reference_count
#     assert 3 == dog.reference_count
#     assert 1 == dog.native_reference_count
#     dog.release()
#     assert 1 == owner.reference_count
#     assert 2 == dog.reference_count
#     assert 1 == dog.native_reference_count
#     dog.release()
#     assert 1 == owner.reference_count
#     assert 1 == owner.native_reference_count
#     assert 1 == dog.reference_count
#     assert 1 == dog.native_reference_count
#     assert not dog.is_invalid
#     owner.say_walk()
#     owner.release()
