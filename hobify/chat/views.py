from django.shortcuts import render,redirect , get_object_or_404
from home.models import Chat, Community, Channel, User
from django.contrib.auth.decorators import login_required
@login_required
def channel(request, community_Id):
    community = Community.objects.filter(community_ID=community_Id).first()
    # If the community does not exist, set channels to an empty queryset
    if community is None:
        channels = Channel.objects.none()  
    # No channels if community doesn't exist
    else:
        # Filter channels that belong to the specified community
        channels = Channel.objects.filter(community=community)
    request.session['community_id'] = community_Id
    request.session['channels'] = [{'id': ch.channel_ID, 'name': ch.channel_name, 'description': ch.description, 'image': ch.channel_image.url} for ch in channels]
    # Pass the filtered channels and community to the template
    return render(request, "channel.html", {
        'channels': channels,
        })
def add_channel(request,community_Id ,username):
    if request.method == 'POST':
        name = request.POST.get('name')
        descr= request.POST.get('descr')
        img = request.FILES.get('image')
        admin= username
        community_instance = Community.objects.get(community_ID=community_Id)
        com = Channel(channel_name=name ,description= descr, channel_image=img,community=community_instance, channel_admin = username)
        com.save()
        redirect('index')
    return render(request, "add_channel.html",{"community_Id":community_Id})
def get_chat(request):
    if request.htmx:
        message = request.POST.get('message')
        request.session['message'] = message
        user = request.user
       
        curr_channel= request.session.get('curr_channel')
        curr_channel= Channel.objects.get(channel_ID=curr_channel)
        chats= Chat(chats=message, user=user, channel=curr_channel)
        chats.save()
        user = request.user
        community_id = request.session.get('community_id')
        # Save the chat message with the user instance
        community = Community.objects.filter(community_ID=community_id).first()# Retrieve all channels within the community
        channels = Channel.objects.filter(community=community)
    # Retrieve chats for the current channel, ordered by chat_time
        chats = Chat.objects.filter(channel=curr_channel).order_by('chat_time')
    return render(request, 'channel.html', {         
            'channels': channels,
            'curr_channel':curr_channel,
            'chats':chats,
        })
def current_channel(request,channel_ID):
        # Get the user instance (ensure it exists)
        community_id = request.session.get('community_id')
        channels_data = request.session.get('channels', [])
        message = request.session.get('message')
        
        user = request.user
        # Save the chat message with the user instance
        community = Community.objects.filter(community_ID=community_id).first()
        curr_channel = get_object_or_404(Channel, channel_ID=channel_ID)
        request.session['curr_channel'] =channel_ID    
    # Retrieve all channels within the community
        channels = Channel.objects.filter(community=community)
    # Retrieve chats for the current channel, ordered by chat_time
        chats = Chat.objects.filter(channel=curr_channel).order_by('chat_time')  
        curr_channel_data = {
    "id": curr_channel.channel_ID,
    "name": curr_channel.channel_name,
    "description": curr_channel.description,
    # Add other fields if necessary
}
        return render(request, 'channel.html', { 
            'channels': channels,
            'curr_channel': curr_channel,
            'chats':chats,
            'curr_channel_data':curr_channel_data,
        })