import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, User, Post


#Schema objects detail post & user
class PostObject(SQLAlchemyObjectType):
    class Meta:
        model = Post
        interfaces = (graphene.relay.Node, )
class UserObject(SQLAlchemyObjectType):
   class Meta:
       model = User
       interfaces = (graphene.relay.Node, )
class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    all_posts = SQLAlchemyConnectionField(PostObject)
    all_users = SQLAlchemyConnectionField(UserObject)

#Schema objects create post
class CreatePost(graphene.Mutation):
    class Input:
        title = graphene.String(required=True)
        body = graphene.String(required=True) 
        authorPost = graphene.String(required=True)
    post = graphene.Field(PostObject)
    def mutate(self, info, title, body, authorPost):
        user = User.query.filter_by(username=str(authorPost)).first()
        post = Post(title=title, body=body)
        if user is not None:
            post.author_post = user.username
            post.author_id = user.uuid
        db_session.add(post)
        db_session.commit()
        return CreatePost(post=post)

class CreateUser(graphene.Mutation):
    class Input:
        username = graphene.String(required=True)
    user = graphene.Field(UserObject)
    def mutate(self, info, username):
        user = User(username=username)
        db_session.add(user)
        db_session.commit()
        return CreateUser(user=user)       

class Mutation(graphene.ObjectType):
    create_post = CreatePost.Field()
    create_user = CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

#EXAMPLE SYNTAQ
# mutation {
#   createUser(username:"arifka"){
#     user{
#       uuid
#       username 
#     }
#   }
# }


# mutation{
#   createPost(authorPost:"candra",title:"judulnya", body:"isinya"){
#     post{
#       authorPost
#       title
#       body
#     }
#   }
# }


# query{
#   allPosts {
#     edges {
#       node {
#         id
#         authorPost
#       }
#     }
#   }
# }