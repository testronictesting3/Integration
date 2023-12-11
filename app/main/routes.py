from app.main import main


@main.route("/", methods=['GET','POST'])
def mainRoute():
    return "Main Route "
