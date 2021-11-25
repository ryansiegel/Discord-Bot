#start round command
@inter_client.slash_command(name="tournament-items", description="Items for tournament staff to use.")
async def roundtimer(inter): 
    pass
@roundtimer.sub_command(name="staff-dispute", description="Allows a staff member to open a dispute for two trainers.", options=[Option("trainer1", "Trainer one in the dispute.", OptionType.USER, required=True), Option("Trainer two in the dispute.", OptionType.USER, required=True)])
async def extendedround(inter, trainer1, trainer2):
    reload(mod)
    channelPrint = bot.get_channel(000000000000000000)
    await mod.staffdispute(inter, channelPrint, bot, trainer1, trainer2)