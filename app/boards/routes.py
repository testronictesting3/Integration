from app.boards import board

@board.route("/" , methods=['GET'])
def index():
    return "Board route"
