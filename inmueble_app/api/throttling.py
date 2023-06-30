from rest_framework.throttling import UserRateThrottle

class CommentCreateThrottle(UserRateThrottle):
    scope = 'comment-create'

class CommentListThrottle(UserRateThrottle):
    scope = 'comment-list'
