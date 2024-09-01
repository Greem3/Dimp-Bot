import marshal, discord, NewSimpleSQL, asyncio

#Variables for not errors
db: NewSimpleSQL.Database = NewSimpleSQL.Database('')
bot: discord.Bot
message: discord.Embed
solution: tuple
solution_id: int
problem_id: int
answer: discord.Message
#//

#Function for not errors
def KeyIn(value1, value2):
    'This is a function.'
#//

answer.add_reaction("✅") #await
answer.add_reaction("❌") #await
answer.add_reaction("🔄") #await

def check(reaction, user):
    return str(reaction.emoji) in ["✅", "❌", "🔄"] and user != bot.user

try:
    reaction, user = 0 #await bot.wait_for("reaction_add", timeout=60.0, check=check)
    reaction: discord.Reaction
    user: discord.User
    
    users_votes: dict = marshal.loads(solution[6])
    
    if not KeyIn(users_votes, user.id):
        
        if str(reaction.emoji) == "✅":
            users_votes[user.id] = "positive"
            db.custom_execute("UPDATE Solutions SET positive_votes = positive_votes + 1, users_votes = ? WHERE id = ? AND problem_id = ?", marshal.dumps(users_votes), solution_id, problem_id)
            
        elif str(reaction.emoji) == "❌":
            users_votes[user.id] = "negative"
            db.custom_execute("UPDATE Solutions SET negative_votes = negative_votes + 1, users_votes = ? WHERE id = ? AND problem_id = ?", marshal.dumps(users_votes), solution_id, problem_id)
        
        new_values = db.simple_select_data("Solutions", f'positive_votes, negative_votes', f'WHERE id = {solution_id} AND problem_id = {problem_id}', True)
            
        message.set_field_at(1, name="Votes:", value=new_values[0]+new_values[1])
        message.set_field_at(2, name="Positive Votes Percentaje:", value=f'{(new_values[0]/(new_values[0] + new_values[1]))*100}%' if new_values[0]+new_values[1] > 0 else "0%")
        
        #await answer.edit(embed=message)
        #return
    
    if str(reaction.emoji) == "🔄":
            
        if KeyIn(users_votes, user.id):
            positive, negative = 0, 0
            
            if users_votes[user.id] == "positive":
                positive += 1
            else:
                negative += 1
                
            users_votes.pop(user.id)
            
            db.custom_execute(f"UPDATE Solutions SET positive_votes = positive_votes - {positive}, negative_votes = negative_votes - {negative}, users_votes = ? WHERE id = ? AND problem_id = ?", marshal.dumps(users_votes), solution_id, problem_id)
            
            new_values = db.simple_select_data("Solutions", f'positive_votes, negative_votes', f'WHERE id = {solution_id} AND problem_id = {problem_id}', True)
            
            message.set_field_at(1, name="Votes:", value=new_values[0]+new_values[1])
            message.set_field_at(2, name="Positive Votes Percentaje:", value=f'{(new_values[0]/(new_values[0] + new_values[1]))*100}%' if new_values[0]+new_values[1] > 0 else "0%")
            
            # await answer.edit(embed=message)
except asyncio.TimeoutError:
    pass