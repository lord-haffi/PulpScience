"""
Contains functions to fill in example data into the sqlite database for testing purposes.
"""
import json
import traceback
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from sqlite3 import Connection, Cursor, connect
from typing import TypedDict

import click
from bidict import bidict

DATABASE_PATH = Path(__file__).parents[1] / "test_db/db.sqlite3"
SAMPLE_CONTENT_PATH = Path(__file__).parent / "sample_content.json"


class SampleContent(TypedDict):
    title: str
    subtitle: str
    content: str
    authors: list[str]
    featuredImage: str
    date: str
    tags: list[str]
    categories: list[str]
    series: str


def create_connection() -> Connection:
    """
    Create a database connection to the SQLite database specified by DATABASE_PATH
    :return: Connection object
    """
    return connect(DATABASE_PATH, isolation_level="DEFERRED")


def create_cursor(connection: Connection) -> Cursor:
    """
    Create a cursor to execute SQL statements
    :param connection: Connection object
    :return: Cursor object
    """
    return connection.cursor()


@lru_cache(maxsize=32)
def load_sample_content() -> list[SampleContent]:
    """
    Load sample content from json file
    """
    return json.load(SAMPLE_CONTENT_PATH.open("r"))


@lru_cache(maxsize=32)
def create_tags(cursor: Cursor) -> bidict[int, str]:
    """
    Create all tags which are used in the sample content
    Returns: Dictionary (tag_id, name)
    """
    sample_content = load_sample_content()
    tags = set(tag for article in sample_content for tag in article["tags"])
    inserted_tags = bidict()
    for tag in tags:
        cursor.execute("INSERT INTO homepage_tag (name) VALUES (?)", (tag,))
        inserted_tags[cursor.lastrowid] = tag
    return inserted_tags


@lru_cache(maxsize=32)
def create_categories(cursor: Cursor) -> bidict[int, str]:
    """
    Create all categories which are used in the sample content
    Returns: Dictionary (category_id, name)
    """
    sample_content = load_sample_content()
    categories = set(category for article in sample_content for category in article["categories"])
    inserted_categories = bidict()
    for category in categories:
        cursor.execute("INSERT INTO homepage_category (name) VALUES (?)", (category,))
        inserted_categories[cursor.lastrowid] = category
    return inserted_categories


@lru_cache(maxsize=32)
def create_users(cursor: Cursor) -> bidict[int, str]:
    """
    Create some example users. All users in the sample content should be created here.
    Returns: Dictionary (user_id, alias)
    """
    users = [
        ("chwag", "Christoph"),
        ("lord_haffi", "Leon"),
        ("daniel_son", "Daniel"),
    ]
    inserted_users = bidict()
    for user in users:
        cursor.execute("INSERT INTO homepage_commentable DEFAULT VALUES")
        commentable_id = cursor.lastrowid
        cursor.execute("INSERT INTO homepage_followable DEFAULT VALUES")
        followable_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO homepage_user (alias, name, commentable_ptr_id, followable_ptr_id) VALUES (?, ?, ?, ?)",
            (*user, commentable_id, followable_id),
        )
        inserted_users[cursor.lastrowid] = user[0]
    return inserted_users


@lru_cache(maxsize=32)
def create_projects(cursor: Cursor) -> bidict[int, str]:
    """
    Create some example projects
    Returns: Dictionary (project_id, title)
    """
    projects = [
        (
            "Pulp Science",
            "Little insights of scientists work",
            "This is a project about science in general.",
            "public",
            ["chwag", "lord_haffi"],
            ["DNA", "quantum computing"],
            ["physics", "biology"],
        ),
        (
            "Unofficial",
            "A sample unofficial project",
            "This is a sample unofficial project (scope private).",
            "private",
            ["lord_haffi"],
            ["computation"],
            ["physics"],
        ),
    ]
    users = create_users(cursor)
    categories = create_categories(cursor)
    tags = create_tags(cursor)
    inserted_projects = bidict()
    for project in projects:
        cursor.execute("INSERT INTO homepage_commentable DEFAULT VALUES")
        commentable_id = cursor.lastrowid
        cursor.execute("INSERT INTO homepage_followable DEFAULT VALUES")
        followable_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO homepage_project ("
            "title, "
            "subtitle, "
            "description, "
            "visibility, "
            "commentable_ptr_id, "
            "followable_ptr_id"
            ") VALUES (?, ?, ?, ?, ?, ?)",
            (*project[:4], commentable_id, followable_id),
        )
        inserted_projects[cursor.lastrowid] = project[0]
        cursor.executemany(
            "INSERT INTO homepage_project_related_authors (project_id, user_id) VALUES (?, ?)",
            [(cursor.lastrowid, users.inv[related_author]) for related_author in project[4]],
        )
        cursor.executemany(
            "INSERT INTO homepage_project_related_tags (project_id, tag_id) VALUES (?, ?)",
            [(cursor.lastrowid, tags.inv[related_tag]) for related_tag in project[5]],
        )
        cursor.executemany(
            "INSERT INTO homepage_project_related_categories (project_id, category_id) VALUES (?, ?)",
            [(cursor.lastrowid, categories.inv[related_category]) for related_category in project[6]],
        )

    return inserted_projects


@lru_cache(maxsize=32)
def create_articles(cursor: Cursor) -> bidict[int, str]:
    """
    Create the articles from the sample content
    Returns: Dictionary (article_id, title)
    """
    sample_content = load_sample_content()
    parent_project_id = create_projects(cursor).inv["Pulp Science"]
    users = create_users(cursor)
    categories = create_categories(cursor)
    tags = create_tags(cursor)
    inserted_articles = bidict()
    max_versionable_group_result = cursor.execute("SELECT MAX(version_group) FROM homepage_versionable").fetchone()
    version_group = max_versionable_group_result[0] + 1 if max_versionable_group_result[0] is not None else 1
    for article in sample_content:
        cursor.execute("INSERT INTO homepage_commentable DEFAULT VALUES")
        commentable_id = cursor.lastrowid
        created_at = datetime.strptime(article["date"], "%d/%m/%Y")
        cursor.execute(
            "INSERT INTO homepage_versionable (version_group, version_number, created)  VALUES (?, ?, ?)",
            (version_group, 1, created_at),
        )
        version_group += 1
        versionable_id = cursor.lastrowid
        cursor.execute(
            "INSERT INTO homepage_article ("
            "title, "
            "subtitle, "
            "content, "
            "visibility, "
            "related_project_id, "
            "commentable_ptr_id, "
            "versionable_ptr_id"
            ") VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                article["title"],
                article["subtitle"],
                article["content"],
                "public",
                parent_project_id,
                commentable_id,
                versionable_id,
            ),
        )
        inserted_articles[cursor.lastrowid] = article["title"]
        cursor.executemany(
            "INSERT INTO homepage_article_related_authors (article_id, user_id) VALUES (?, ?)",
            [(cursor.lastrowid, users.inv[related_author]) for related_author in article["authors"]],
        )
        cursor.executemany(
            "INSERT INTO homepage_article_related_tags (article_id, tag_id) VALUES (?, ?)",
            [(cursor.lastrowid, tags.inv[related_tag]) for related_tag in article["tags"]],
        )
        cursor.executemany(
            "INSERT INTO homepage_article_related_categories (article_id, category_id) VALUES (?, ?)",
            [(cursor.lastrowid, categories.inv[related_category]) for related_category in article["categories"]],
        )

    return inserted_articles


def wipe_database(cursor: Cursor):
    """
    Wipe the database
    """
    cursor.execute("DELETE FROM homepage_article_related_categories")
    cursor.execute("DELETE FROM homepage_article_related_tags")
    cursor.execute("DELETE FROM homepage_article_related_authors")
    cursor.execute("DELETE FROM homepage_article")
    cursor.execute("DELETE FROM homepage_project_related_categories")
    cursor.execute("DELETE FROM homepage_project_related_tags")
    cursor.execute("DELETE FROM homepage_project_related_authors")
    cursor.execute("DELETE FROM homepage_project")
    cursor.execute("DELETE FROM homepage_comment")
    cursor.execute("DELETE FROM homepage_user")
    cursor.execute("DELETE FROM homepage_category")
    cursor.execute("DELETE FROM homepage_tag")
    cursor.execute("DELETE FROM homepage_versionable")
    cursor.execute("DELETE FROM homepage_followable")
    cursor.execute("DELETE FROM homepage_commentable")


def generate_test_data(wipe: bool):
    print("Connecting to SQLite database.")
    conn = create_connection()
    cursor = create_cursor(conn)
    try:
        if wipe:
            print("Wiping database.")
            wipe_database(cursor)
            conn.commit()
        print("Creating tags.")
        create_tags(cursor)
        print("Creating categories.")
        create_categories(cursor)
        print("Creating users.")
        create_users(cursor)
        print("Creating projects.")
        create_projects(cursor)
        print("Creating articles.")
        create_articles(cursor)
        print("Committing changes.")
        conn.commit()
    except Exception as e:
        print(traceback.format_exc())
        print("Rolling back changes.")
        conn.rollback()
        exit(1)
    finally:
        print("Closing connection.")
        conn.close()
    print("Done.")


@click.command()
@click.option("--wipe", is_flag=True, help="Wipe the database before generating test data.")
def click_generate_test_data(wipe: bool):
    """
    Click command to generate test data.
    """
    generate_test_data(wipe)


if __name__ == "__main__":
    click_generate_test_data()


def test_generate_test_data():
    """
    Test if the test data can be generated without errors.
    """
    generate_test_data(wipe=True)
