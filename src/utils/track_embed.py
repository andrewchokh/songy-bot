import nextcord


def make_embed(title, url, color, thumbnail_url, action, author, duration, requester, pos_queue = None):
    emb = nextcord.Embed(
        title=title,
        url=url,
        color=color
    )
    emb.set_thumbnail(url=thumbnail_url)
    emb.set_author(name=action)
    
    fields = [
        {
            'name': 'Author', 
            'value': author, 
            'inline': True
        },
        {
            'name': 'Track Duration', 
            'value': duration, 
            'inline': True
        },
        {
            'name': 'Requested by', 
            'value': requester, 
            'inline': True
        },
        {
            'name': 'Position in Queue', 
            'value': pos_queue, 
            'inline': False
        }
    ]

    for field in fields:
        if field['value'] is None: continue

        emb.add_field(
            name=field['name'], 
            value=field['value'], 
            inline=field['inline']
        )    
    
    return emb