import requests
import os

# Disable SSL verification by manipulating environment variables
# os.environ['REQUESTS_CA_BUNDLE'] = 'src/ca-cert.crt'

class ChatwootAPIError(Exception):
    pass

class ChatwootSDK:
    def __init__(self, base_url, platform_access_token, api_access_token):
        self.base_url = base_url
        self.headers = {
            'api_access_token': api_access_token,
            'Content-Type': 'application/json'
        }

        self.platform_access_token = platform_access_token
        self.api_access_token = api_access_token
        self.accounts = self.Accounts(self)
        self.agent_bots = self.AgentBots(self)
        self.users = self.Users(self)
        self.inboxes = self.Inboxes(self)
        self.contacts = self.Contacts(self)
        self.conversations = self.Conversations(self)
        self.messages = self.Messages(self)
        self.teams = self.Teams(self)
        self.custom_filters = self.CustomFilters(self)
        self.webhooks = self.Webhooks(self)
        self.custom_attributes = self.CustomAttributes(self)
        self.automation_rules = self.AutomationRules(self)
        self.portals = self.Portals(self)
        self.reports = self.Reports(self)

    def _send_request(self, method, endpoint, data=None, json=None, params=None):
        url = f"{self.base_url}{endpoint}"
        if("public" == endpoint.split("/")[1]):
            if("api_access_token" in self.headers):
                del self.headers['api_access_token']
        elif("api" == endpoint.split("/")[1]):
            self.headers['api_access_token'] = self.api_access_token
        elif("platform" == endpoint.split("/")[1]):
            self.headers['api_access_token'] = self.platform_access_token
        response = requests.request(method, url, headers=self.headers, data=data, json=json)

        if response.status_code >= 400:
            raise ChatwootAPIError(f"Error {response.status_code}: {response.text}")

        return response.json()

    class Accounts:
        def __init__(self, client):
            self.client = client

        def create(self, name):
            return self.client._send_request('POST', '/platform/api/v1/accounts', json={'name': name})

        def get(self, account_id):
            return self.client._send_request('GET', f'/platform/api/v1/accounts/{account_id}')

        def update(self, account_id, name):
            return self.client._send_request('PATCH', f'/platform/api/v1/accounts/{account_id}', json={'name': name})

        def delete(self, account_id):
            return self.client._send_request('DELETE', f'/platform/api/v1/accounts/{account_id}')

        def list_account_users(self, account_id):
            return self.client._send_request('GET', f'/platform/api/v1/accounts/{account_id}/account_users')

        def create_account_user(self, account_id, user_id, role):
            return self.client._send_request('POST', f'/platform/api/v1/accounts/{account_id}/account_users', json={'user_id': user_id, 'role': role})

        def delete_account_user(self, account_id, user_id):
            return self.client._send_request('DELETE', f'/platform/api/v1/accounts/{account_id}/account_users', json={'user_id': user_id})

    class AgentBots:
        def __init__(self, client):
            self.client = client

        def list(self):
            return self.client._send_request('GET', '/platform/api/v1/agent_bots')

        def create(self, name, description, outgoing_url):
            return self.client._send_request('POST', '/platform/api/v1/agent_bots', json={'name': name, 'description': description, 'outgoing_url': outgoing_url})

        def get(self, bot_id):
            return self.client._send_request('GET', f'/platform/api/v1/agent_bots/{bot_id}')

        def update(self, bot_id, name=None, description=None, outgoing_url=None):
            data = {}
            if name:
                data['name'] = name
            if description:
                data['description'] = description
            if outgoing_url:
                data['outgoing_url'] = outgoing_url
            return self.client._send_request('PATCH', f'/platform/api/v1/agent_bots/{bot_id}', json=data)

        def delete(self, bot_id):
            return self.client._send_request('DELETE', f'/platform/api/v1/agent_bots/{bot_id}')

    class Users:
        def __init__(self, client):
            self.client = client

        def create(self, name, email, password, custom_attributes=None):
            data = {
                'name': name,
                'email': email,
                'password': password
            }
            if custom_attributes:
                data['custom_attributes'] = custom_attributes
            return self.client._send_request('POST', '/platform/api/v1/users', json=data)

        def get(self, user_id):
            return self.client._send_request('GET', f'/platform/api/v1/users/{user_id}')

        def update(self, user_id, name=None, email=None, password=None, custom_attributes=None):
            data = {}
            if name:
                data['name'] = name
            if email:
                data['email'] = email
            if password:
                data['password'] = password
            if custom_attributes:
                data['custom_attributes'] = custom_attributes
            return self.client._send_request('PATCH', f'/platform/api/v1/users/{user_id}', json=data)

        def delete(self, user_id):
            return self.client._send_request('DELETE', f'/platform/api/v1/users/{user_id}')

        def get_login_url(self, user_id):
            return self.client._send_request('GET', f'/platform/api/v1/users/{user_id}/login')

    class Inboxes:
        def __init__(self, client):
            self.client = client

        def get_details(self, inbox_identifier):
            return self.client._send_request('GET', f'/public/api/v1/inboxes/{inbox_identifier}')

        def list(self, account_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/inboxes')

        def get(self, account_id, inbox_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/inboxes/{inbox_id}/')

        def create(self, account_id, name, channel_type, website_url=None, welcome_title=None, welcome_tagline=None, agent_away_message=None, widget_color=None):
            data = {
                'name': name,
                'channel': {
                    'type': channel_type
                }
            }
            if website_url:
                data['channel']['website_url'] = website_url
            if welcome_title:
                data['channel']['welcome_title'] = welcome_title
            if welcome_tagline:
                data['channel']['welcome_tagline'] = welcome_tagline
            if agent_away_message:
                data['channel']['agent_away_message'] = agent_away_message
            if widget_color:
                data['channel']['widget_color'] = widget_color
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/inboxes/', json=data)

        def update(self, account_id, inbox_id, name=None, enable_auto_assignment=None, avatar_url=None, channel_data=None):
            data = {}
            if name:
                data['name'] = name
            if enable_auto_assignment is not None:
                data['enable_auto_assignment'] = enable_auto_assignment
            if avatar_url:
                data['avatar'] = avatar_url
            if channel_data:
                data['channel'] = channel_data
            return self.client._send_request('PATCH', f'/api/v1/accounts/{account_id}/inboxes/{inbox_id}', json=data)

        def get_agent_bot(self, account_id, inbox_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/inboxes/{inbox_id}/agent_bot')

        def set_agent_bot(self, account_id, inbox_id, agent_bot_id):
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/inboxes/{inbox_id}/set_agent_bot', json={'agent_bot': agent_bot_id})

        def list_members(self, account_id, inbox_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/inbox_members/{inbox_id}')

        def add_member(self, account_id, inbox_id, user_ids):
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/inbox_members', json={'inbox_id': inbox_id, 'user_ids': user_ids})

        def update_members(self, account_id, inbox_id, user_ids):
            return self.client._send_request('PATCH', f'/api/v1/accounts/{account_id}/inbox_members', json={'inbox_id': inbox_id, 'user_ids': user_ids})

        def delete_member(self, account_id, inbox_id, user_ids):
            return self.client._send_request('DELETE', f'/api/v1/accounts/{account_id}/inbox_members', json={'inbox_id': inbox_id, 'user_ids': user_ids})

    class Contacts:
        def __init__(self, client):
            self.client = client

        def create(self, inbox_identifier, identifier, identifier_hash=None, email=None, name=None, phone_number=None, avatar_url=None, custom_attributes=None):
            data = {
                'identifier': identifier
            }
            if identifier_hash:
                data['identifier_hash'] = identifier_hash
            if email:
                data['email'] = email
            if name:
                data['name'] = name
            if phone_number:
                data['phone_number'] = phone_number
            if avatar_url:
                data['avatar_url'] = avatar_url
            if custom_attributes:
                data['custom_attributes'] = custom_attributes
            return self.client._send_request('POST', f'/public/api/v1/inboxes/{inbox_identifier}/contacts', json=data)

        def get(self, inbox_identifier, contact_identifier):
            return self.client._send_request('GET', f'/public/api/v1/inboxes/{inbox_identifier}/contacts/{contact_identifier}')

        def update(self, inbox_identifier, contact_identifier, identifier=None, identifier_hash=None, email=None, name=None, phone_number=None, avatar_url=None, custom_attributes=None):
            data = {}
            if identifier:
                data['identifier'] = identifier
            if identifier_hash:
                data['identifier_hash'] = identifier_hash
            if email:
                data['email'] = email
            if name:
                data['name'] = name
            if phone_number:
                data['phone_number'] = phone_number
            if avatar_url:
                data['avatar_url'] = avatar_url
            if custom_attributes:
                data['custom_attributes'] = custom_attributes
            return self.client._send_request('PATCH', f'/public/api/v1/inboxes/{inbox_identifier}/contacts/{contact_identifier}', json=data)

        def list(self, account_id, sort=None, page=1):
            params = {'page': page}
            if sort:
                params['sort'] = sort
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/contacts', params=params)

        def create_contact(self, account_id, inbox_id, name=None, email=None, phone_number=None, avatar_url=None, identifier=None, custom_attributes=None):
            data = {
                'inbox_id': inbox_id
            }
            if name:
                data['name'] = name
            if email:
                data['email'] = email
            if phone_number:
                data['phone_number'] = phone_number
            if avatar_url:
                data['avatar_url'] = avatar_url
            if identifier:
                data['identifier'] = identifier
            if custom_attributes:
                data['custom_attributes'] = custom_attributes
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/contacts', json=data)

        def get_contact(self, account_id, contact_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/contacts/{contact_id}')

        def update_contact(self, account_id, contact_id, name=None, email=None, phone_number=None, avatar_url=None, identifier=None, custom_attributes=None):
            data = {}
            if name:
                data['name'] = name
            if email:
                data['email'] = email
            if phone_number:
                data['phone_number'] = phone_number
            if avatar_url:
                data['avatar_url'] = avatar_url
            if identifier:
                data['identifier'] = identifier
            if custom_attributes:
                data['custom_attributes'] = custom_attributes
            return self.client._send_request('PUT', f'/api/v1/accounts/{account_id}/contacts/{contact_id}', json=data)

        def delete_contact(self, account_id, contact_id):
            return self.client._send_request('DELETE', f'/api/v1/accounts/{account_id}/contacts/{contact_id}')

        def search(self, account_id, query, sort=None, page=1):
            params = {
                'q': query,
                'page': page
            }
            if sort:
                params['sort'] = sort
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/contacts/search', params=params)

        def filter(self, account_id, payload, page=1):
            data = {
                'payload': payload
            }
            params = {'page': page}
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/contacts/filter', json=data, params=params)

        def get_conversations(self, account_id, contact_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/contacts/{contact_id}/conversations')

        def create_contact_inbox(self, account_id, contact_id, inbox_id, source_id=None):
            data = {
                'inbox_id': inbox_id
            }
            if source_id:
                data['source_id'] = source_id
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/contacts/{contact_id}/contact_inboxes', json=data)

        def get_contact_inboxes(self, account_id, contact_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/contacts/{contact_id}/contactable_inboxes')

    class Conversations:
        def __init__(self, client):
            self.client = client

        def create(self, inbox_identifier, contact_identifier, custom_attributes=None):
            data = {}
            if custom_attributes:
                data['custom_attributes'] = custom_attributes
            return self.client._send_request('POST', f'/public/api/v1/inboxes/{inbox_identifier}/contacts/{contact_identifier}/conversations', json=data)

        def list(self, inbox_identifier, contact_identifier):
            return self.client._send_request('GET', f'/public/api/v1/inboxes/{inbox_identifier}/contacts/{contact_identifier}/conversations')
        def list_all(self, account_id, assignee_type='all', status='open', page=1, labels=None, team_id=None):
            params = {
                'assignee_type': assignee_type,
                'status': status,
                'page': page
            }
            if labels:
                params['labels'] = labels
            if team_id:
                params['team_id'] = team_id
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/conversations', params=params)

        def create_conversation(self, account_id, source_id, inbox_id, contact_id=None, additional_attributes=None, custom_attributes=None, status=None, assignee_id=None, team_id=None, content=None, message_type=None):
            data = {
                'source_id': source_id,
                'inbox_id': inbox_id
            }
            if contact_id:
                data['contact_id'] = contact_id
            if additional_attributes:
                data['additional_attributes'] = additional_attributes
            if custom_attributes:
                data['custom_attributes'] = custom_attributes
            if status:
                data['status'] = status
            if assignee_id:
                data['assignee_id'] = assignee_id
            if team_id:
                data['team_id'] = team_id
            if content:
                data['message'] = {
                    'content': content
                }
                if message_type:
                    data['message']['message_type'] = message_type
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/conversations', json=data)

        def filter(self, account_id, payload, page=1):
            data = {
                'payload': payload
            }
            params = {'page': page}
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/conversations/filter', json=data, params=params)

        def get(self, account_id, conversation_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/conversations/{conversation_id}')

        def toggle_status(self, account_id, conversation_id, status):
            data = {
                'status': status
            }
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_status', json=data)

        def toggle_priority(self, account_id, conversation_id, priority):
            data = {
                'priority': priority
            }
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/conversations/{conversation_id}/toggle_priority', json=data)

        def assign(self, account_id, conversation_id, assignee_id=None, team_id=None):
            data = {}
            if assignee_id:
                data['assignee_id'] = assignee_id
            if team_id:
                data['team_id'] = team_id
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/conversations/{conversation_id}/assignments', json=data)

        def list_labels(self, account_id, conversation_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/conversations/{conversation_id}/labels')

        def add_labels(self, account_id, conversation_id, labels):
            data = {
                'labels': labels
            }
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/conversations/{conversation_id}/labels', json=data)

    class Messages:
        def __init__(self, client):
            self.client = client

        def create(self, inbox_identifier, contact_identifier, conversation_id, content, echo_id=None):
            data = {
                'content': content
            }
            if echo_id:
                data['echo_id'] = echo_id
            return self.client._send_request('POST', f'/public/api/v1/inboxes/{inbox_identifier}/contacts/{contact_identifier}/conversations/{conversation_id}/messages', json=data)

        def list(self, inbox_identifier, contact_identifier, conversation_id):
            return self.client._send_request('GET', f'/public/api/v1/inboxes/{inbox_identifier}/contacts/{contact_identifier}/conversations/{conversation_id}/messages')

        def update(self, inbox_identifier, contact_identifier, conversation_id, message_id, submitted_values):
            data = {
                'submitted_values': submitted_values
            }
            return self.client._send_request('PATCH', f'/public/api/v1/inboxes/{inbox_identifier}/contacts/{contact_identifier}/conversations/{conversation_id}/messages/{message_id}', json=data)

        def list_all(self, account_id, conversation_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages')

        def create_message(self, account_id, conversation_id, content, message_type='outgoing', private=False, content_type=None, content_attributes=None, attachment_blob=None, sender_type=None, sender_id=None):
            data = {
                'content': content,
                'message_type': message_type,
                'private': private
            }
            if content_type:
                data['content_type'] = content_type
            if content_attributes:
                data['content_attributes'] = content_attributes
            if attachment_blob:
                data['attachment'] = attachment_blob
            if sender_type:
                data['sender_type'] = sender_type
            if sender_id:
                data['sender_id'] = sender_id
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages', json=data)

        def delete_message(self, account_id, conversation_id, message_id):
            return self.client._send_request('DELETE', f'/api/v1/accounts/{account_id}/conversations/{conversation_id}/messages/{message_id}')

    class Teams:
        def __init__(self, client):
            self.client = client

        def list(self, account_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/teams')

        def create(self, account_id, name, description=None, allow_auto_assign=None):
            data = {
                'name': name
            }
            if description:
                data['description'] = description
            if allow_auto_assign is not None:
                data['allow_auto_assign'] = allow_auto_assign
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/teams', json=data)

        def get(self, account_id, team_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/teams/{team_id}')

        def update(self, account_id, team_id, name=None, description=None, allow_auto_assign=None):
            data = {}
            if name:
                data['name'] = name
            if description:
                data['description'] = description
            if allow_auto_assign is not None:
                data['allow_auto_assign'] = allow_auto_assign
            return self.client._send_request('PATCH', f'/api/v1/accounts/{account_id}/teams/{team_id}', json=data)

        def delete(self, account_id, team_id):
            return self.client._send_request('DELETE', f'/api/v1/accounts/{account_id}/teams/{team_id}')

        def list_members(self, account_id, team_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/teams/{team_id}/team_members')

        def add_member(self, account_id, team_id, user_ids):
            data = {
                'user_ids': user_ids
            }
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/teams/{team_id}/team_members', json=data)

        def update_members(self, account_id, team_id, user_ids):
            data = {
                'user_ids': user_ids
            }
            return self.client._send_request('PATCH', f'/api/v1/accounts/{account_id}/teams/{team_id}/team_members', json=data)

        def delete_member(self, account_id, team_id, user_ids):
            data = {
                'user_ids': user_ids
            }
            return self.client._send_request('DELETE', f'/api/v1/accounts/{account_id}/teams/{team_id}/team_members', json=data)

    class CustomFilters:
        def __init__(self, client):
            self.client = client

        def list(self, account_id, filter_type=None):
            params = {}
            if filter_type:
                params['filter_type'] = filter_type
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/custom_filters', params=params)

        def create(self, account_id, name, filter_type, query):
            data = {
                'name': name,
                'type': filter_type,
                'query': query
            }
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/custom_filters', json=data)

        def get(self, account_id, custom_filter_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}')

        def update(self, account_id, custom_filter_id, name=None, filter_type=None, query=None):
            data = {}
            if name:
                data['name'] = name
            if filter_type:
                data['type'] = filter_type
            if query:
                data['query'] = query
            return self.client._send_request('PATCH', f'/api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}', json=data)

        def delete(self, account_id, custom_filter_id):
            return self.client._send_request('DELETE', f'/api/v1/accounts/{account_id}/custom_filters/{custom_filter_id}')

    class Webhooks:
        def __init__(self, client):
            self.client = client

        def list(self, account_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/webhooks')

        def create(self, account_id, url, subscriptions):
            data = {
                'url': url,
                'subscriptions': subscriptions
            }
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/webhooks', json=data)

        def update(self, account_id, webhook_id, url=None, subscriptions=None):
            data = {}
            if url:
                data['url'] = url
            if subscriptions:
                data['subscriptions'] = subscriptions
            return self.client._send_request('PATCH', f'/api/v1/accounts/{account_id}/webhooks/{webhook_id}', json=data)

        def delete(self, account_id, webhook_id):
            return self.client._send_request('DELETE', f'/api/v1/accounts/{account_id}/webhooks/{webhook_id}')

    class CustomAttributes:
        def __init__(self, client):
            self.client = client

        def list(self, account_id, attribute_model):
            params = {
                'attribute_model': attribute_model
            }
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/custom_attribute_definitions', params=params)

        def create(self, account_id, attribute_display_name, attribute_display_type, attribute_description, attribute_key, attribute_values, default_value, attribute_model):
            data = {
                'attribute_display_name': attribute_display_name,
                'attribute_display_type': attribute_display_type,
                'attribute_description': attribute_description,
                'attribute_key': attribute_key,
                'attribute_values': attribute_values,
                'default_value': default_value,
                'attribute_model': attribute_model
            }
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/custom_attribute_definitions', json=data)

        def get(self, account_id, custom_attribute_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/custom_attribute_definitions/{custom_attribute_id}')

        def update(self, account_id, custom_attribute_id, attribute_display_name=None, attribute_display_type=None, attribute_description=None, attribute_key=None, attribute_values=None, default_value=None, attribute_model=None):
            data = {}
            if attribute_display_name:
                data['attribute_display_name'] = attribute_display_name
            if attribute_display_type:
                data['attribute_display_type'] = attribute_display_type
            if attribute_description:
                data['attribute_description'] = attribute_description
            if attribute_key:
                data['attribute_key'] = attribute_key
            if attribute_values:
                data['attribute_values'] = attribute_values
            if default_value:
                data['default_value'] = default_value
            if attribute_model:
                data['attribute_model'] = attribute_model
            return self.client._send_request('PATCH', f'/api/v1/accounts/{account_id}/custom_attribute_definitions/{custom_attribute_id}', json=data)

        def delete(self, account_id, custom_attribute_id):
            return self.client._send_request('DELETE', f'/api/v1/accounts/{account_id}/custom_attribute_definitions/{custom_attribute_id}')

    class AutomationRules:
        def __init__(self, client):
            self.client = client

        def list(self, account_id, page=1):
            params = {'page': page}
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/automation_rules', params=params)

        def create(self, account_id, name, description, event_name, conditions, actions):
            data = {
                'name': name,
                'description': description,
                'event_name': event_name,
                'conditions': conditions,
                'actions': actions
            }
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/automation_rules', json=data)

        def get(self, account_id, rule_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/automation_rules/{rule_id}')

        def update(self, account_id, rule_id, name=None, description=None, event_name=None, conditions=None, actions=None):
            data = {}
            if name:
                data['name'] = name
            if description:
                data['description'] = description
            if event_name:
                data['event_name'] = event_name
            if conditions:
                data['conditions'] = conditions
            if actions:
                data['actions'] = actions
            return self.client._send_request('PATCH', f'/api/v1/accounts/{account_id}/automation_rules/{rule_id}', json=data)

        def delete(self, account_id, rule_id):
            return self.client._send_request('DELETE', f'/api/v1/accounts/{account_id}/automation_rules/{rule_id}')

    class Portals:
        def __init__(self, client):
            self.client = client

        def create(self, account_id, name, slug, archived=None, color=None, config=None, custom_domain=None, header_text=None, homepage_link=None, page_title=None):
            data = {
                'name': name,
                'slug': slug
            }
            if archived is not None:
                data['archived'] = archived
            if color:
                data['color'] = color
            if config:
                data['config'] = config
            if custom_domain:
                data['custom_domain'] = custom_domain
            if header_text:
                data['header_text'] = header_text
            if homepage_link:
                data['homepage_link'] = homepage_link
            if page_title:
                data['page_title'] = page_title
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/portals', json=data)

        def list(self, account_id):
            return self.client._send_request('GET', f'/api/v1/accounts/{account_id}/portals')

        def update(self, account_id, archived=None, color=None, config=None, custom_domain=None, header_text=None, homepage_link=None, name=None, slug=None, page_title=None):
            data = {}
            if archived is not None:
                data['archived'] = archived
            if color:
                data['color'] = color
            if config:
                data['config'] = config
            if custom_domain:
                data['custom_domain'] = custom_domain
            if header_text:
                data['header_text'] = header_text
            if homepage_link:
                data['homepage_link'] = homepage_link
            if name:
                data['name'] = name
            if slug:
                data['slug'] = slug
            if page_title:
                data['page_title'] = page_title
            return self.client._send_request('PATCH', f'/api/v1/accounts/{account_id}/portals', json=data)

        def create_category(self, account_id, portal_id, name, slug, locale, description=None, position=None, associated_category_id=None, parent_category_id=None):
            data = {
                'name': name,
                'slug': slug,
                'locale': locale
            }
            if description:
                data['description'] = description
            if position:
                data['position'] = position
            if associated_category_id:
                data['associated_category_id'] = associated_category_id
            if parent_category_id:
                data['parent_category_id'] = parent_category_id
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/portals/{portal_id}/categories', json=data)

        def create_article(self, account_id, portal_id, title, slug, content, meta=None, position=None, status=None, views=None, author_id=None, category_id=None, folder_id=None, associated_article_id=None):
            data = {
                'title': title,
                'slug': slug,
                'content': content
            }
            if meta:
                data['meta'] = meta
            if position:
                data['position'] = position
            if status:
                data['status'] = status
            if views:
                data['views'] = views
            if author_id:
                data['author_id'] = author_id
            if category_id:
                data['category_id'] = category_id
            if folder_id:
                data['folder_id'] = folder_id
            if associated_article_id:
                data['associated_article_id'] = associated_article_id
            return self.client._send_request('POST', f'/api/v1/accounts/{account_id}/portals/{portal_id}/articles', json=data)

    class Reports:
        def __init__(self, client):
            self.client = client

        def get(self, account_id, metric, since, until, id=None, type=None):
            params = {
                'metric': metric,
                'since': since,
                'until': until
            }
            if id:
                params['id'] = id
            if type:
                params['type'] = type
            return self.client._send_request('GET', f'/api/v2/accounts/{account_id}/reports', params=params)

        def get_summary(self, account_id, since, until, id=None, type=None):
            params = {
                'since': since,
                'until': until
            }
            if id:
                params['id'] = id
            if type:
                params['type'] = type
            return self.client._send_request('GET', f'/api/v2/accounts/{account_id}/reports/summary', params=params)

        def get_account_conversation_metrics(self, account_id):
            return self.client._send_request('GET', f'/api/v2/accounts/{account_id}/reports/conversations', params={'type': 'account'})

        def get_agent_conversation_metrics(self, account_id, user_id):
            return self.client._send_request('GET', f'/api/v2/accounts/{account_id}/reports/conversations/', params={'type': 'agent', 'user_id': user_id})
