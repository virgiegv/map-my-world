from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from src.location_and_categories import schemas
from src.location_and_categories import crud

def test_create_simple_category(db_session) -> None:
    """Test that checks if a single category can be created"""
    result = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    assert result["detail"].name == "testCategory"

def test_get_simple_category_by_id(db_session) -> None:
    """Test that checks if a single category can be obtained through the api using its id"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    result = crud.get_category(db_session,category["detail"].id)
    assert ((category["detail"].name == result.name)and(category["detail"].id == result.id))

def test_get_simple_category_by_incorrect_id(db_session) -> None:
    """Test that checks that when the id that was asked for doesnt exist, the result is none"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    result = crud.get_category(db_session, 17345)
    assert (result == None)

def test_get_category_by_name_one_result_one_member_list(db_session) -> None:
    """Test that checks if a single category can be obtained through the api from a table that only has one member"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    result = crud.get_category_by_name(db_session,"testCategory")
    assert ((category["detail"].name == result[0].name)and(category["detail"].id == result[0].id))

def test_get_category_by_name_one_result_two_member_list(db_session) -> None:
    """Test that checks if a single category can be obtained through the api from a table that only has 2 members"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    crud.create_category(db_session,schemas.CategoryCreate(name="incorrectResponse"))
    result = crud.get_category_by_name(db_session,"testCategory")
    assert ((category["detail"].name == result[0].name)and(category["detail"].id == result[0].id))

def test_get_category_by_name_two_result_two_member_list(db_session) -> None:
    """Test that checks if two categories can be obtained through the api from a table that has 2 categories"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    secondCategory = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory2"))
    result = crud.get_category_by_name(db_session,"testCategory")
    assert ((category["detail"].name == result[0].name)and
            (category["detail"].id == result[0].id)and
            (secondCategory["detail"].name == result[1].name)and
            (secondCategory["detail"].id == result[1].id))

def test_get_category_by_name_zero_result_two_member_list(db_session) -> None:
    """Test that checks if a obtaining no results from looking in the category table responds appropriately"""
    crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    crud.create_category(db_session,schemas.CategoryCreate(name="testCategory2"))
    result = crud.get_category_by_name(db_session,"badEntry")
    assert (len(result) == 0)

def test_get_all_categories(db_session) -> None:
    """Test that checks if one can get all categories from a table with 3 categories"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    secondCategory = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory2"))
    thirdCategory = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory3"))
    result = crud.get_all_categories(db_session)
    assert ((category["detail"].name == result[0].name)and
            (category["detail"].id == result[0].id)and
            (secondCategory["detail"].name == result[1].name)and
            (secondCategory["detail"].id == result[1].id)and
            (thirdCategory["detail"].name == result[2].name)and
            (thirdCategory["detail"].id == result[2].id))

def test_update_category(db_session) -> None:
    """Test that checks if one can update a single category"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    crud.update_category(db_session,schemas.CategoryCreate(name="updatedTestCategory"),category["detail"].id)
    result = crud.get_category(db_session,category["detail"].id)
    assert (result.name == "updatedTestCategory")

def test_delete_category(db_session) -> None:
    """Test that checks if one can delete a single category"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    crud.delete_category(db_session,category["detail"].id)
    result = crud.get_category(db_session,category["detail"].id)
    assert (result == None)

def test_delete_category(db_session) -> None:
    """Test that checks if one can delete a single category"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    crud.delete_category(db_session,category["detail"].id)
    result = crud.get_category(db_session,category["detail"].id)
    assert (result == None)

def test_create_simple_location(db_session) -> None:
    """Test that checks if a single location can be created"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    result = crud.create_location(db_session,schemas.LocationCreate(name="testLocation", latitude = 246, longitude = 93456),category["detail"].id)
    assert ((result["detail"].name == "testLocation")and(result["detail"].latitude == 246)and(result["detail"].longitude == 93456))

def test_get_simple_location_by_id(db_session) -> None:
    """Test that checks if a single category can be obtained through the api using its id"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    location = crud.create_location(db_session,schemas.LocationCreate(name="testLocation", latitude = 2257, longitude = 43216),category["detail"].id)
    result = crud.get_location(db_session,location["detail"].id)
    assert ((result.name == "testLocation")and(result.latitude == 2257)and(result.longitude == 43216))

def test_get_simple_location_by_id(db_session) -> None:
    """Test that checks if a single category can be obtained through the api using its id"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    location = crud.create_location(db_session,schemas.LocationCreate(name="testLocation", latitude = 2257, longitude = 43216),category["detail"].id)
    result = crud.get_location(db_session,location["detail"].id)
    assert ((result.name == "testLocation")and(result.latitude == 2257)and(result.longitude == 43216))


def test_get_simple_location_by_incorrect_id(db_session) -> None:
    """Test that checks that when the id that was asked for doesnt exist, the result is none"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    crud.create_location(db_session,schemas.LocationCreate(name="testLocation", latitude = 2257, longitude = 43216),category["detail"].id)
    result = crud.get_location(db_session, 1737345)
    assert (result == None)

def test_get_location_by_name_one_result_one_member_list(db_session) -> None:
    """Test that checks if a single location can be obtained through the api from a table that only has one member"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    location = crud.create_location(db_session,schemas.LocationCreate(name="testLocation", latitude = 27, longitude = 426),category["detail"].id)
    result = crud.get_location_by_name(db_session,"testLocation")
    assert ((result[0].name == "testLocation")and(result[0].latitude == 27)and(result[0].longitude == 426))

def test_get_location_by_name_one_result_two_member_list(db_session) -> None:
    """Test that checks if a single location can be obtained through the api from a table that only has 2 members"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    location = crud.create_location(db_session,schemas.LocationCreate(name="testLocation", latitude = 27, longitude = 426,),category["detail"].id)
    secondLocation = crud.create_location(db_session,schemas.LocationCreate(name="wrongEntry", latitude = 5427, longitude = 42875686),category["detail"].id)
    result = crud.get_location_by_name(db_session,"testLocation")
    assert ((location["detail"].name == result[0].name)and(location["detail"].id == result[0].id))

def test_get_location_by_name_two_result_two_member_list(db_session) -> None:
    """Test that checks if two locations can be obtained through the api from a table that has 2 locations"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    location = crud.create_location(db_session,schemas.LocationCreate(name="testLocation", latitude = 27, longitude = 426,),category["detail"].id)
    secondLocation = crud.create_location(db_session,schemas.LocationCreate(name="testLocation2", latitude = 5427, longitude = 42875686),category["detail"].id)
    result = crud.get_location_by_name(db_session,"testLocation")
    assert ((location["detail"].name == result[0].name)and
            (location["detail"].id == result[0].id)and
            (secondLocation["detail"].name == result[1].name)and
            (secondLocation["detail"].id == result[1].id))

def test_get_location_by_name_zero_result_two_member_list(db_session) -> None:
    """Test that checks if a obtaining no results from looking in the category table responds appropriately"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    crud.create_location(db_session,schemas.LocationCreate(name="testLocation", latitude = 5427, longitude = 42875686),category["detail"].id)
    crud.create_location(db_session,schemas.LocationCreate(name="testLocation2", latitude = 5427, longitude = 42875686),category["detail"].id)
    result = crud.get_category_by_name(db_session,"badEntry")
    assert (len(result) == 0)

def test_get_all_locations(db_session) -> None:
    """Test that checks if one can get all categories from a table with 3 categories"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    location = crud.create_location(db_session,schemas.LocationCreate(name="testLocation", latitude = 27, longitude = 426,),category["detail"].id)
    secondLocation = crud.create_location(db_session,schemas.LocationCreate(name="testLocation2", latitude = 5427, longitude = 42875686),category["detail"].id)
    thirdLocation = crud.create_location(db_session,schemas.LocationCreate(name="testLocation3", latitude = 5432427, longitude = 428771),category["detail"].id)
    result = crud.get_all_locations(db_session)
    assert ((location["detail"].name == result[0].name)and
            (location["detail"].id == result[0].id)and
            (secondLocation["detail"].name == result[1].name)and
            (secondLocation["detail"].id == result[1].id)and
            (thirdLocation["detail"].name == result[2].name)and
            (thirdLocation["detail"].id == result[2].id))
    
def test_update_location(db_session) -> None:
    """Test that checks if one can update a single category"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    category2 = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory2"))
    location = crud.create_location(db_session,schemas.LocationCreate(name="testLocation", latitude = 27, longitude = 426),category["detail"].id)
    crud.update_location(db_session,schemas.LocationUpdate(name="UpdatedTestLocation", latitude = 1228, longitude = 6222, category_id = category2["detail"].id),location["detail"].id)
    result = crud.get_location(db_session,location["detail"].id)
    assert ((result.name == "UpdatedTestLocation")and
            (result.latitude == 1228)and
            (result.longitude == 6222)and
            (result.category_id == category2["detail"].id))
    
def test_delete_location(db_session) -> None:
    """Test that checks if one can delete a single category"""
    category = crud.create_category(db_session,schemas.CategoryCreate(name="testCategory"))
    location = crud.create_location(db_session,schemas.LocationCreate(name="testLocation", latitude = 27, longitude = 426),category["detail"].id)
    crud.delete_location(db_session,location["detail"].id)
    result = crud.get_location(db_session,category["detail"].id)
    assert (result == None)
