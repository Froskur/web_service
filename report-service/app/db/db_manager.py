from app.db.db import database


async def get_reports_summary():
    query = """
        select routes.id,
            routes."name", 
            routes.short_num,
            routes.created_at,
            routes.updated_at,	   
            routes.author_id,
            users."name" user_name,
            users.last_login,
            ( select count(*) from routes_has_points where route_id = routes.id) points_count
        from routes
        join users on users.id = routes.author_id 
        join routes_has_points on routes_has_points.route_id = routes.id 
        group by routes.author_id, routes.id, users."name", users.last_login
        ;
    """

    return await database.fetch_all(query=query)


