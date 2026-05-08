import json
import os
from typing import List, Dict, Any
from collections import Counter


def createTopTags(json_file: Dict, num_of_tags: int, url: str) -> str:
    """ creates html for the most common tags """
    temp_container: List[str] = []
    tags: List[List[str]] = [json_file[posts]["tags"] for posts in json_file]
    cleanded_tags: List[str] = [tag for nested_tags in tags for tag in nested_tags]
    for c in Counter(cleanded_tags).most_common(num_of_tags):
        html_list: str = f'<tag class="button is-danger">{c[0]} {c[1]}</tag>'
        temp_container.append(html_list)
    result: str = "\n".join(temp_container)
    return result


def createPostsList(json_file: Dict, url: str, type: str) -> str:
    """ creates html listing for every post in the json_file """
    temp_container: Dict = {}
    for posts in json_file:
        post_type: str = json_file[posts]["type"]
        post_date: str = json_file[posts]["date"]
        post_year: str = post_date[:4]
        post_path: str = f'{url}/posts/{posts.split(".")[0]}.html'
        post_title: str = json_file[posts]["title"].title()
        post_data: List[str] = [post_date,post_path,post_title]
        if post_type == type:
            if post_year in temp_container:
                temp_container[post_year].append(post_data)
            else:
                temp_container[post_year] = [post_data]

    result: List[str] = []    
    for year, post_row in temp_container.items():
        html_year_top: str = f'''
        <h3 class="has-text-left has-text-centered-mobile">{year}</h3>
            <div class="block has-text-left">
                <ul>
        '''
        html_year_bottom: str = '''
            </ul>
        </div>
        '''
        result.append(html_year_top)
        for post in post_row:
            html_list: str = f'<li><span class="tag">{post[0]}</span> &emsp; <a class="has-text-danger" href="{post[1]}">{post[2]}</a></li>'
            result.append(html_list)
        
        result.append(html_year_bottom)
    result = "\n".join(result)
    return result


def createPostsIndex(html_template: str,template_folder: str,target_folder: str,tags: str,posts: str) -> str:
    """ creates the posts.html page """
    with open(os.path.join(html_template,"custom_main.html"), "r") as template_file:
        main_html: str = template_file.read()
    with open(os.path.join(template_folder,"template_page_posts.html"), "r") as template_file:
        posts_list_html: str = template_file.read()

    posts_list_html: str = (
        posts_list_html
        .replace("{{placeholder_top_tags}}",tags)
        .replace("{{placeholder_all_posts}}",posts)
    )
    result = main_html.replace(
        "{{placeholder_content}}",posts_list_html
    )
    return result


def createPostsPage(json_path: str, num_of_tags: int, url: str, html_template: str,template_folder: str,target_folder: str) -> None:
    """ composer for creating the posts overview page """
    with open(json_path,"r",encoding="utf8") as file_json:
        json_as_string: str = file_json.read()
        json_posts: Dict = json.loads(json_as_string)
    
    top_tags: str = createTopTags(json_posts, num_of_tags, url)
    posts_list: str = createPostsList(json_posts, url, "article")
    page_html = createPostsIndex(html_template,template_folder,target_folder,top_tags,posts_list)

    with open(os.path.join(target_folder,"pages","posts.html"), "w", encoding="utf8") as template_file:
        template_file.write(page_html)


def createArticlesPage(json_path: str, num_of_tags: int, url: str, html_template: str,template_folder: str,target_folder: str) -> None:
    """ composer for creating the articles overview page """
    with open(json_path,"r",encoding="utf8") as file_json:
        json_as_string: str = file_json.read()
        json_posts: Dict = json.loads(json_as_string)

    top_tags: str = createTopTags(json_posts, num_of_tags, url)
    posts_list: str = createPostsList(json_posts, url, "article")
    page_html = createPostsIndex(html_template,template_folder,target_folder,top_tags,posts_list)

    with open(os.path.join(target_folder,"pages","articles.html"), "w", encoding="utf8") as template_file:
        template_file.write(page_html)


def createProjectsPage(json_path: str, num_of_tags: int, url: str, html_template: str,template_folder: str,target_folder: str) -> None:
    """ composer for creating the articles overview page """
    with open(json_path,"r",encoding="utf8") as file_json:
        json_as_string: str = file_json.read()
        json_posts: Dict = json.loads(json_as_string)

    top_tags: str = createTopTags(json_posts, num_of_tags, url)
    posts_list: str = createPostsList(json_posts, url, "project")
    page_html = createPostsIndex(html_template,template_folder,target_folder,top_tags,posts_list)

    with open(os.path.join(target_folder,"pages","projects.html"), "w", encoding="utf8") as template_file:
        template_file.write(page_html)


def createLatestArticles(json_file: Dict, num_of_articles: int, url: str) -> str:
    temp_container: List[str] = []
    for posts in json_file: 
      post_title: str = json_file[posts]["title"].title()
      post_path: str = f"{url}/posts/{posts.split('.')[0]}.html"
      post_date: str = json_file[posts]["date"]
      html_list: str = f'<li><span class="tag">{post_date}</span> &emsp;<a class="has-text-danger" href="{post_path}">{post_title}</a></li>'
      temp_container.append(html_list)
    result: str = "\n".join(temp_container[:num_of_articles])
    return result


def getFeaturedArticles(json_file: Dict, url: str) -> str:
    temp_container: List[str] = []
    for posts in json_file:
      if json_file[posts]["featured"] is True:
        post_title: str = json_file[posts]["title"].title()
        post_path: str = f"{url}/posts/{posts.split('.')[0]}.html"
        post_summary: str = json_file[posts]["summary"]
        html_cell: str = f"""
        <div class="cell">
          <div class="card">
            <header class="card-header">
              <p class="card-header-title">
                {post_title}
              </p>
            </header>
            <div class="card-content">
              <div class="content">
                {post_summary}
              </div>
            </div>
            <footer class="card-footer">
              <a href="{post_path}" class="card-footer-item has-text-danger">Read more</a>
            </footer>
          </div>
        </div>
        """
        temp_container.append(html_cell)
    result: str = "\n".join(temp_container)
    return result


def createIndex(html_template: str,template_folder: str,target_folder: str,latest,featured) -> None:
    with open(os.path.join(html_template,"custom_main.html"), "r") as template_file:
        main_html: str = template_file.read()
    with open(os.path.join(template_folder,"template_home.html"), "r") as template_file:
        home_html: str = template_file.read()

    home_html: str = (
        home_html
        .replace("{{placeholder_latest_articles}}",latest)
        .replace("{{placeholder_featured_articles}}",featured)
    )
    result = main_html.replace(
        "{{placeholder_content}}",home_html
    )

    with open(os.path.join(target_folder,"index.html"), "w") as template_file:
        template_file.write(result)


def createHome(json_path: str, num_of_articles: int, url: str, html_template: str,template_folder: str,target_folder: str) -> None:
    with open(json_path,"r") as file_json:
        json_as_string: str = file_json.read()
        json_posts: Dict = json.loads(json_as_string)

    latest_articles: str = createLatestArticles(json_posts,num_of_articles,url)
    featured_articles: str = getFeaturedArticles(json_posts,url)
    createIndex(html_template,template_folder,target_folder,latest_articles,featured_articles)


def createAbout(html_template: str, template_folder: str, target_folder: str) -> None:
    with open(os.path.join(html_template,"custom_main.html"), "r") as template_file:
        main_html: str = template_file.read()
    with open(os.path.join(template_folder,"template_about.html"), "r") as template_file:
        about_html: str = template_file.read()
    result: str = main_html.replace("{{placeholder_content}}",about_html)

    with open(os.path.join(target_folder,"pages","about.html"), "w") as template_file:
        template_file.write(result)
    

def createExtras(html_template: str, template_folder: str, target_folder: str) -> None:
    with open(os.path.join(html_template,"custom_main.html"), "r") as template_file:
        main_html: str = template_file.read()
    with open(os.path.join(template_folder,"template_extras.html"), "r") as template_file:
        extras_html: str = template_file.read()
    result: str = main_html.replace("{{placeholder_content}}",extras_html)

    with open(os.path.join(target_folder,"pages","extras.html"), "w") as template_file:
        template_file.write(result)
    