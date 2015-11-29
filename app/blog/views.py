from app import redis
from flask import render_template, request, redirect, url_for
import markdown2
from . import blog


@blog.route('/')
def index():
    posts = []
    for post_id in redis.lrange('post:post-list', 0, -1):
        post = redis.hgetall('post:%s' % post_id)
        posts.append(post)
    return render_template('blog/index.html', posts=posts)


@blog.route('/tags/<string:tag_str>')
def tag_index(tag_str):
    posts = []
    post_ids = redis.smembers("post:post-tags:%s" % tag_str)
    post_ids = [int(post_id) for post_id in post_ids]
    post_ids.sort()
    for post_id in post_ids:
        post = redis.hgetall('post:%s' % post_id)
        posts.append(post)
    return render_template('blog/index.html', posts=posts)


@blog.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'GET':
        return render_template('blog/new.html')

    title = request.form['title']
    content = request.form['content']
    tags = request.form['tags']

    post_id = redis.incr('post:post-id')
    pipe = redis.pipeline()
    pipe.hmset('post:%s' % post_id,
                {
                    "id": post_id,
                    "title": title,
                    "content": content,
                    "content_markdown": markdown2.markdown(content, extras=['fenced-code-blocks']),
                    "tags": tags
                })

    for tag in tags.split(','):
        pipe.sadd('post:post-tags:%s' % tag.strip(), post_id)

    pipe.rpush('post:post-list', post_id)
    pipe.execute()
    return redirect(url_for('.detail', post_id=post_id))


@blog.route('/detail/<int:post_id>')
def detail(post_id):
    post = redis.hgetall('post:%s' % post_id)
    return render_template('blog/detail.html', post=post)


@blog.route('/update/<int:post_id>/markdown')
def update_markdown(post_id):
    content = redis.hget('post:%s' % post_id, 'content')
    content_markdown = markdown2.markdown(content, extras=['fenced-code-blocks'])
    redis.hset('post:%s' % post_id, 'content_markdown', content_markdown)
    return redirect(url_for('.detail', post_id=post_id))
