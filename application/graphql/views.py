# -*- coding: utf-8 -*-

from flask_graphql import GraphQLView
from flask_security import current_user


class GraphQLViewCurrentUser(GraphQLView):

    def get_context(self, request):
        context = super().get_context(request)
        context.update({'current_user': current_user})
        return context
