from flask import Flask, render_template
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)

# visualisasi graphql 
app.add_url_rule('/graphql',
			view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

@app.route('/')
def index():
	return "Go to /graphql"

if __name__ == "__main__":
	app.run(port=5001, debug = True)
