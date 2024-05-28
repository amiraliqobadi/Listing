from fastapi import APIRouter, Depends, HTTPException, Path, Request
from starlette import status
from models import User, Listing
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal
from .auth import get_current_user
from fastapi.encoders import jsonable_encoder
from routers.auth import limiter

router = APIRouter(
	prefix='/listing',
	tags=['listing']
)



def get_db():
	"""
	A function that returns a database session.
	It yields the database session and
	"""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class ListingRequest(BaseModel):
	type: Literal['apartment', 'house'] = Field(...)
	availableNow: bool
	address: str = Field(min_length=0)




@router.get('/', status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def read_all(request: Request, user: user_dependency, db: db_dependency):
	"""
	A description of the entire function,
	its parameters, and its return types.
	"""
	if user is None:
		raise HTTPException(status_code=401, detail='Authentication Failed')
	
	
	return jsonable_encoder(db.query(Listing).filter(user.get('id') == Listing.ownerId).all())


@router.get("/Listing/{list_id}", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def read_list(request: Request, db: db_dependency, list_id: int = Path(gt=0)):
	"""
	Reads a list from the database by the provided list_id.

	Parameters:
	- db: Dependency injection for database connection.
	- list_id: The ID of the list to be retrieved from the database (must be greater than 0).

	Returns:
	- JSON representation of the retrieved list model.

	Raises:
	- HTTPException: If the list with the given list_id is not found, raises a 404 error.
	"""
	list_model = db.query(Listing).filter(Listing.id == list_id).first()
	
	if list_model is not None:
		return jsonable_encoder(list_model)
	
	raise HTTPException(status_code=404, detail='Not found any Listing')


@router.post('/', status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def create_listing(request: Request, user: user_dependency, listing_request: ListingRequest, db: db_dependency):
	"""
	Create a new listing using the provided user, listing request, and database dependencies.

	:param request:
	:param db:
	:param listing_request:
	:param user: The user dependency
	"""
	if user is None:
		raise HTTPException(status_code=401, detail='Authentication Failed')
	listing = Listing(
		type=listing_request.type,
		availableNow=listing_request.availableNow,
		address=listing_request.address,
		ownerId=user.get('id')
	)
	db.add(listing)
	db.commit()
	return jsonable_encoder(listing)


@router.put('/listing/{list_id}', status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
def update_list(request: Request, user: user_dependency, db: db_dependency, list_request: ListingRequest, list_id: int = Path(gt=0)):
	"""
	Update a specific list with the provided data.

	Parameters:
	- user: a dependency for user information
	- db: a dependency for database operations
	- list_request: the data to update the list with
	- list_id: the identifier of the list to update

	Returns:
	- None
	"""
	list_model = db.query(Listing).filter(Listing.id == list_id and User.id == user.get('id')).first()
	
	if list_model is None:
		raise HTTPException(status_code=404, detail='List not found')
	
	if list_request.type is not None:
		list_model.type = list_request.type
	
	if list_request.availableNow is not None:
		list_model.availableNow = list_request.availableNow
	
	if list_request.address is not None:
		list_model.address = list_request.address
	
	list_model.UpdatedAt = datetime.now()
	
	db.add(list_model)
	db.commit()


@router.delete("/list/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")
def delete_list(request: Request, user: user_dependency, db: db_dependency, list_id: int = Path(gt=0)):
	"""
	Delete a list item based on the provided list_id.

	:param user: User dependency
	:param db: Database dependency
	:param list_id: The id of the list item to be deleted
	"""
	list_model = db.query(Listing).filter(Listing.id == list_id and User.id == user.get('id')).first()
	if list_model is None:
		raise HTTPException(status_code=404, detail="List Not Found")
	db.query(Listing).filter(list_id == Listing.id).delete()
	
	db.commit()
	
	