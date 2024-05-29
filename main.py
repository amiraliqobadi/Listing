import uvicorn
from pathlib import Path
from database import engine
import models


def get_next_count(file_path):
    """
    A function that takes a file path as input,
    reads a number from that file, increments the number by 1,
    and writes the updated number back to the file. Returns the updated number.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        with open(file_path, 'w') as f:
            f.write('0')
    if file_path.exists():
        with open(file_path, 'r') as f:
            try:
                counter = int(f.read().strip())
            except ValueError:
                counter = 0
    else:
        counter = 0
    counter += 1
    with open(file_path, 'w') as f:
        f.write(str(counter))
    return counter


if __name__ == "__main__":
    count = get_next_count('count.txt')
    models.Base.metadata.create_all(bind=engine)
    uvicorn.run('config:app', host='0.0.0.0', port=3000, reload=True)
    
    
    