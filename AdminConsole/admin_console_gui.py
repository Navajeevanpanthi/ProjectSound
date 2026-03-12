import sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
from app import app
if __name__=="__main__":
    print("Open http://127.0.0.1:5000")
    app.run(debug=True,port=5000)
