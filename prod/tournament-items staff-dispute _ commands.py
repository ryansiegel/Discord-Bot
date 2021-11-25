async def staffdispute(inter, channelPrint, bot, trainer1, trainer2):
    currentDB = 'HIDDEN INFORMATION'
    valid_roles = [y.name.lower() for y in inter.author.roles]
    yesRole = 'no'
    connection = pymysql.connect(user='INSERT USER HERE', password='INSERT PASSWORD HERE', db=currentDB)  # open connection to mysql
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM general LIMIT 1')
    data = list(str(cursor.fetchall()).replace("'","").replace("(","").replace(")","").split(","))
    currentCount = int(data[1])
    toID = int(data[2])
    if toID != 9999:
        to_role = inter.guild.get_role(toID)
        to_rolee = str(inter.guild.get_role(toID)).lower()
        for item in valid_roles:
            if item == to_rolee or inter.author.guild_permissions.administrator:
                yesRole = 'yes'
    else:
        to_role = get(inter.guild.roles, name="Tournament Staff")
        for item in valid_roles:
            if inter.author.guild_permissions.administrator:
                yesRole = 'yes'
    if yesRole == 'yes':
        train1 = await bot.fetch_user(trainer1.id)
        train2 = await bot.fetch_user(trainer2.id)
        bot_role = get(inter.guild.members, name="Seagull's Assistant")
        overwrites = {
            inter.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            inter.author: discord.PermissionOverwrite(read_messages=True),
            to_role: discord.PermissionOverwrite(read_messages=True),
            bot_role: discord.PermissionOverwrite(read_messages=True),
            trainer1: discord.PermissionOverwrite(read_messages=True),
            trainer2: discord.PermissionOverwrite(read_messages=True)}
        channelName = 'battle-dispute-' + str(currentCount)
        channel = await inter.guild.create_text_channel(channelName, overwrites=overwrites)
        channel1 = discord.utils.get(inter.guild.channels, name=channelName)
        embedVar = discord.Embed(title="Dispute", description=train1.mention + ' & ' + train2.mention  + ' - head to ' + channel1.mention + ' to discuss your dispute. Thanks!', color=0x000000)
        await inter.reply(embed=embedVar)
        embedVar1 = discord.Embed(title="Dispute", description='Trainers and tournament staff, ' + str(inter.author) + ' has made a dispute on behalf of the trainers having an issue.\nTrainers, please send evidence that would help support your dispute such as screenshots or video via a online streaming service (for example: Streamable or YouTube) so the tournament staff can make a decision.', color=0x000000)
        await channel1.send(embed=embedVar1)
        await channel1.send(to_role.mention + ' ' + train1.mention + ' ' + train2.mention)
        currentCount += 1
        currentCount = str(currentCount)
        await channelPrint.send('Staff Dispute - ' + str(inter.guild.name) + ' - ' + str(inter.author) + '.')
        try:
            cursor.execute("UPDATE general set currentNum=" + currentCount + " where numHold=1")
            connection.commit()
        except:
            connection.rollback()
            await channelPrint.send('DB item currentnum for disputes has failed to update for server ' + inter.guild.name + '.') #send to seagulls discord
    else:
        await inter.reply('Command failed, required role not on user.')
        await channelPrint.send('Staff Dispute not used by a staff member ' + inter.guild.name + ' - ' + str(inter.author) + '.') #send to seagulls discord
    connection.close()
