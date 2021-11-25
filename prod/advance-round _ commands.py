async def advance(inter, channelPrint, bot):
    currentDB = str('server' + str(inter.guild.id))
    connection = pymysql.connect(user='root', password='Se@gu11B0t!!', db=currentDB)  # open connection to mysql
    cursor = connection.cursor()
    try:
        print('test')
        cursor.execute('SELECT * FROM general LIMIT 1')
        data = list(str(cursor.fetchall()).replace("'","").replace("(","").replace(")","").split(","))
        toID = int(data[2])
        to_role = []
        if toID != 9999:
            to_role = inter.guild.get_role(toID)
            embedVar = discord.Embed(title="Advance Round", description="TO's, the advance round command has been triggered meaning the round is ready to advance. Please advance the round when possible.", color=0x000000)
            await inter.reply(embed=embedVar)
            await inter.channel.send(to_role.mention) #tags roles
        else:
            for roleSS in inter.guild.roles:
                to_role.append(roleSS)
            to_role = to_role[-1]
            embedVar = discord.Embed(title="Advance Round", description="TO's, the advance round command has been triggered meaning the round is ready to advance. Please advance the round when possible.\n\n**NOTICE:** There is no set Tournament Staff role on the bot. Head to the admin channel and do a ***/set*** command to complete this.", color=0x000000)
            await inter.reply(embed=embedVar)
            await inter.channel.send(to_role.mention) #tags roles
        await channelPrint.send('Advance round - ' + str(inter.guild.name) + '.') #send to seagulls discord
    except:
        connection.rollback()
        await channelPrint.send('Failed to grab db info for TO on server ' + inter.guild.name + '.') #send to seagulls discord
    connection.close()