from nicegui import ui, APIRouter, Client

from pages.sections.CallToAction import call_to_action, PricingCard
from pages.sections.Features import features
from pages.sections.Footer import footer
from pages.sections.Headline import headline
from pages.sections.Showcase import showcase


router = APIRouter()

features_data = [
    {
        'title': 'AI powered analysis',
        'description': 'Confidentier uses cutting edge AI to get insights on your speech.',
        'icon': 'quickreply'
    },
    {
        'title': 'Find Mistakes',
        'description': 'Catch mistakes in your speech and get feedback on how to avoid them.',
        'icon': 'feedback'
    },
    {
        'title': 'Improve your speech',
        'description': 'Confidentier will analyze your speech and give you suggestions to connect with your audience.',
        'icon': 'recommend'
    },
    {
        'title': 'Prepare yourself in advance',
        'description': 'Get possible questions that your audience may have and prepare yourself to tackle them.',
        'icon': 'psychology_alt'
    },
    {
        'title': 'Get insights on your audience',
        'description': 'Understand your audience better and tailor your speech to their needs.',
        'icon': 'groups'
    },
    {
        'title': 'Get key ideas from your speech',
        'description': 'Confidentier will summarize your speech and give you the key ideas to show you what people is getting from your presentation.',
        'icon': 'vpn_key'
    }


]

pricing_cards = [
    PricingCard(
        plan_name='Free',
        price='$0',
        price_periodicity='month',
        price_description='Just want to improve',
        features=[
            'AI powered analysis and suggestions',
            '5 Credits (1 credit = 1 video)',
            'limited to 5 minutes per video',
        ],
        button_text='Signup for free',
        button_link='/login'
    ),
    PricingCard(
        plan_name='Pro',
        price='$19.99',
        price_periodicity='lifetime access',
        price_description='Get the most out of Confidentier',
        features=[
            'Life time access',
            'AI powered analysis and suggestions',
            'unlimited credits',
            'up to 30 minutes per video',
            'Get early access to new features',
            '20% goes to nicegui development support'
        ],  
        button_text='Upgrade to Pro',
        button_link='/login'
    )
]

@router.page('/')
def landing_page(client: Client):
    client.layout.classes('bg-black')
    ui.query('.nicegui-content').classes('p-0')
    headline(
        tag_line=['With', 'Confidentier', 'Never fail a presentation again'], 
        description='With Confidentier you can analyze your speech and get feedback on how to improve it.',
        primary_button_text='Get started',
        secondary_button_text='Learn more',
        primary_button_func=lambda: ui.navigate.to('/login'),
        secondary_button_func=lambda: ui.navigate.to(target='#features')
        )
    features("Get to know Confidentier", features_data)
    showcase("See how it works",
             "Confidentier can take a video or audio of your presentation, talk, or any idea that you want to share and level up with AI that helps you to improve and present it in the best way and connect with your audience. ",
             'https://www.youtube.com/embed/bpWFvhipLKY?si=UAf6PSqQhYSnOjw1')
    call_to_action(
        description='Get started on our free plan and upgrade when you are ready',
        cards=pricing_cards,
        call_to_action_title='Ready to get started?',
        call_to_action_description='Get started on our free plan and upgrade when you are ready.',
        call_to_action_link='/login'
    )
    footer(
        company_name='Confidentier',
        resources=[{'name': 'Login', 'link': '/login'}, {'name': 'App', 'link': '/video'}],
        support=[{'name': 'Contact Us', 'link': 'mailto:programandoconyeicob@gmail.com'}],
        contact_us=[{'name': 'Email', 'link': 'mailto:programandoconyeicob@gmail.com'}],
        rights_reserved='© Copyright 2020. All Rights Reserved.'
    )
    with ui.page_sticky(x_offset=18, y_offset=18):
        ui.html('<a href="https://www.producthunt.com/posts/confidentier?embed=true&utm_source=badge-featured&utm_medium=badge&utm_souce=badge-confidentier" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=488539&theme=light" alt="Confidentier - Sharpen&#0032;your&#0032;presentation&#0032;skills | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>')