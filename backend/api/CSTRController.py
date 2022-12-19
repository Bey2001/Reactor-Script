from flask_restful import Api, Resource, reqparse

class CSTRAdiabaticApiHandler(Resource):

  def get(self):
    parser = reqparse.RequestParser()

    # Parse the query args
    parser.add_argument('lowerTemp', type=float)
    parser.add_argument('upperTemp', type=float)
    parser.add_argument('cA', type=float)
    parser.add_argument('hfA', type=float)
    parser.add_argument('cB', type=float)
    parser.add_argument('hfB', type=float)
    parser.add_argument('cC', type=float)
    parser.add_argument('hfC', type=float)

    args = parser.parse_args()

    print(args)

    # Check to make sure nothing is empty
    return {"status": "Success", "message": str(args)}