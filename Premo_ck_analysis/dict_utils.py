import re
from vader_analysis_utils import sentiment_score

md_hdr = re.compile(r'<!--[a-z]*\n[\s\S]*?\n-->')
ireg = re.compile(r'\!\[Image\]\(https?://\S+|www\.\S+')
url_reg = re.compile(r'\(*https?://\S+|www\.\S+\)*')
brackets_reg = re.compile(r'\[[\W\w\s\d]+\]')
code_reg = re.compile(r'```\s*[a-z]*\n[\s\S]*?\n*```')
md_quoting = re.compile(r'> .*\n')
html_reg = re.compile(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
date_reg = re.compile(r'On\s\d+\s\w+\s\d+\s\d+\:\d+')
user_mention = re.compile(r'\@[\w\-?]+')
regex = [md_hdr, user_mention, brackets_reg, ireg, url_reg, code_reg, md_quoting, html_reg]

def comment_routine(pr) :
    """Routine function that calls the comment-related functions

    Args:
        pr (PullRequest): The current PullRequest object

    Returns:
        unsanitized_comments (list) : the original comments of the PR
        cleaned_comments (list) : the sanitized comments of the PR 
        valence (list[dict]) : list of the valence (Vader) for each comment of the PR 
        
        None if the current PR has no comments or if the api fails to fetch them
    """
    cleaned_comments = []
    valence_list = []
    
    unsanitized_comments, pr_comments = extract_comments(pr)
    if len(pr_comments) < 1 :
        return None, None, None
    
    for com in pr_comments :
        #cleaned = sanitize_text(com)
        cleaned_comments.append(com)
        valence_dict = sentiment_score(com)
        valence_list.append(valence_dict)

    return  unsanitized_comments, cleaned_comments, valence_list

def sanitize_text(text : str) :
    """sanitizes the text

    Args:
        text (str): a PR comment, that is

    Returns:
        cleaned_text (str) : the sanitized comment
    
    Note
        Regex are iterated over to find patterns to remove inside the text (markdown quotes, code blocks,...), to minimize bias during sentiment analysis
    """
    #iterate through regex patterns
    for reg in regex :
        if reg == user_mention :
            replacement = '@User'
        elif reg != date_reg :
            replacement = ''
        
        found_patterns = re.findall(reg, text)
        if len(found_patterns) > 0 :
            for fp in found_patterns :
                text = text.replace(fp, replacement)
                
            #only taking first sentence if comment is a @githubnotification answer
            if (reg == date_reg) :
                text = text.split(r'[:.\s]+')[0]
                   # "".join(filter(lambda c: c != fp, text))
        
            
    #Remove Markdown quoting and whitespaces left
    text = "".join(filter(lambda c: c != "`" and c != "\n" , text))
    return text


def extract_comments(PR ) :
    """Gets comments from the PR

    Args:
        issue_or_PR (PullRequest): the current PullRequest object

    Returns:
        list of original and cleaned comments
    """
    comments = []
    unsanitized_comments = []
    all_comments = PR.get_comments()
    if all_comments.totalCount < 1 :
        all_comments = PR.get_issue_comments()
    
    
    if all_comments.totalCount > 0 :
        for comment in all_comments :
            com_body = comment.body
            unsanitized_comments.append(com_body)
            
            com_body = sanitize_text(com_body)  
            comments.append(com_body)
    return unsanitized_comments, comments


def get_PR_metadata( repo , pr, data_dict : dict, modified_class_files : int) :
    """Gets metadata about the repository and current pull request

    Args:
        repo : the project name (owner/name)
        pr (PullRequest): the current PullRequest object
        data_dict (dict): the dictionnary containing the data about the current PR
        modified_class_files (list) : list of the modified classes by the PR

    Returns:
        data_dict : the updated data dictionnary of the current PR
    """
    meta_dict = {}
    meta_dict["org"] =  repo.owner.login
    meta_dict["project_name"] = repo.name
    meta_dict['PR_id'] = pr.id
    meta_dict['PR_number'] = pr.number
    meta_dict['PR_url'] = pr.html_url
    meta_dict['PR_state'] = pr.state
    meta_dict['PR_is_merged'] = pr.merged
    meta_dict['PR_additions'] = pr.additions
    meta_dict['PR_deletions'] = pr.deletions
    meta_dict['PR_changed_files'] = pr.changed_files
    meta_dict['PR_modified_class_files'] = modified_class_files
    meta_dict['PR_creation'] = pr.created_at.isoformat()
    meta_dict['Base_SHA'] = pr.base.sha
    meta_dict['Head_SHA'] = pr.head.sha
    meta_dict['PR_nb_comments'] = pr.comments
    
    data_dict["Meta"] = meta_dict
    
    return data_dict

