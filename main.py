from requests import get, post
import base64
import json

wp_user = 'aouwal'
wp_password = '11iq Rkmb Tltc Q2io z8Qd JL1x'
wp_credential = f'{wp_user}:{wp_password}'
wp_token = base64.b64encode(wp_credential.encode())
wp_headers = {'Authorization':f'Basic {wp_token.decode("utf-8")}'}




server_url = 'https://mobile-phone-server.vercel.app/phones'
res = get(server_url)
if res.status_code == 200:
    data = res.json()
    phones = data.get('RECORDS')


def media_from_url(img_src,phone_name):
    """
    This will return the wordpress media code from url
    """
    codes = f'<!-- wp:image {{"align":"center","sizeSlug":"large"}} -->' \
            f'<figure class="wp-block-image aligncenter size-large">' \
            f'<img src="{img_src}" alt="{phone_name} image"/>' \
            f'<figcaption>{phone_name}</figcaption></figure>' \
            f'<!-- /wp:image -->'
    return codes


def wp_table_dict(dictionary):
    """
        This wil generate wordpress gutenberg table code from dictionary
    :param dictionary:
    :return: html table string
    """
    codes = '<!-- wp:table --><figure class="wp-block-table"><table><tbody>'
    for key, value in dictionary.items():
        tr_data = f'<tr><td>{key}</td><td>{value}</td></tr>'
        codes += tr_data
    codes += '</tbody></table></figure><!-- /wp:table -->'
    return codes


def wp_paragraph(text):
    """
    This wil generate wordpress gutenberg paragraph code
    """
    codes = f'<!-- wp:paragraph --><p>{text}</p><!-- /wp:paragraph -->'
    return codes


def wp_heading_two(text):
    return f'<!-- wp:heading --><h2>{text}</h2><!-- /wp:heading -->'


def concatenate_string(*args):
    final = ''
    for arg in args:
        final += arg
    return final

def slugify(name):
    code = name.strip().replace(' ','-')
    return code


def create_wp_post(title, content, slug, excerpt, status = 'publish'):
    api_url = 'https://localhost/word/wp-json/wp/v2/posts'
    data = {
        'title': title,
        'content' : content,
        'slug': slug,
        'status': status,
        'excerpt': excerpt
    }
    response = post(api_url, headers=wp_headers, json=data, verify=False)
    print(f'{title} is posted')


for phone in phones:
    name = phone.get("name").title()
    released_at = phone.get('released_at').lower().replace("Released ", '')
    chipset = phone.get("chipset")
    body = phone.get("body")
    os = phone.get("os")
    picture = phone.get('picture')

    first_dictionary ={
        'Name':name,
        'Released at': released_at,
        'Chipset': chipset,
        'Body':body
    }

    first_paragraph = f'{name} has been {released_at}. ' \
                      f'It comes with {chipset} chipset. The body of this mobile is{body}' \
                      f'{os} is the built in android version. '
    article_paragraph = wp_paragraph(first_paragraph)
    first_image = media_from_url(picture, name )
    first_heading = wp_heading_two(f'{name} Overview')
    first_table = wp_table_dict(first_dictionary)

    # Specification Section
    second_heading = wp_heading_two('Specifications')
    specifications_string = phone.get('specifications')
    specifications = json.loads(specifications_string)
    second_table = wp_table_dict(specifications)
    content = concatenate_string(article_paragraph,first_image,first_heading,first_table,
                                 second_heading,second_table)
    slug = slugify(name)
    create_wp_post(name,content,slug,first_paragraph)