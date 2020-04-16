def get_item_to_helper_map(needy_persons, helpers):
	
	item_to_helper_map = {}

	for helper in helpers:
		for item in helper.donated_items:
			if item.menu_item_id in item_to_helper_map :
				item_to_helper_map[item.menu_item_id].append(helper.user_id)
			else:
				item_to_helper_map[item.menu_item_id] = [helper.user_id]
	return item_to_helper_map

def get_helpful_index(person, item_to_helper_map, helpers_index):

	helpful_index = {}

	for item in person.needs:
			if item.menu_item_id in item_to_helper_map:
				for user_id in item_to_helper_map[item.menu_item_id]:
					helper = helpers_index[user_id]
					matched_item =  [x for x in helper.donated_items if x.menu_item_id == item.menu_item_id][0]

					if helper.user_id in helpful_index :
						helpful_index[helper.user_id ].append(matched_item) 
					else:
						helpful_index [helper.user_id ] = [matched_item]

	return helpful_index

def update(helpful_index, menu_item_id):

	new_helpful_index = {}
	for helper in helpful_index:
		result = list( filter(lambda x : x.menu_item_id != menu_item_id,helpful_index[helper]))

		if result:
			new_helpful_index[helper] = result

	return new_helpful_index


def generateMapping(needy_persons,helpers):
	# Assuming needy is sorted according to priority
	# needy_persons [{ user_id:  [(requested_item_id,menu_item_id).....
	# helpers [{user_id: [(donated_item_id, menu_item_id).....
	
	
	requested_to_donated_item_map = {}
	needy_to_helper_map={}
	helper_to_needy_map = {}
	helpers_index = {x.user_id: x for x in helpers}
	item_to_helper_map = get_item_to_helper_map(needy_persons,helpers)
	
	for person in needy_persons:
		
		# map of helper to relevant items that he/she can help needy with 
		helpful_index  = get_helpful_index(person, item_to_helper_map, helpers_index)
		
		print(f'needy ={person.user_id} items_requested = {person.needs} ')

		# when helper has some items that the needy needs
		while person.needs and helpful_index :

			max_items_provided_count = 0
			items_donated_by_best_match = None
			best_match = None

			# finds person with max no. of items
			for user_id, matched_donated_items in helpful_index.items():
				if len(matched_donated_items) > max_items_provided_count:
					max_items_provided_count = len(matched_donated_items)
					items_donated_by_best_match = matched_donated_items
					best_match = user_id
			if person.user_id in needy_to_helper_map:
				needy_to_helper_map[person.user_id].append({best_match : items_donated_by_best_match })  
			else:
				needy_to_helper_map[person.user_id] = [{best_match : items_donated_by_best_match }]
			
			print(f'helpful_index')
			for k,v in helpful_index.items():
				print(k,v)
			print()
			print(f'helper={best_match} item_count = {max_items_provided_count}')
			
			# updates helper_to_needy_map
			if not best_match in helper_to_needy_map:
				helper_to_needy_map[best_match] = [person.user_id]
			elif person.user_id not in helper_to_needy_map[best_match]:
				helper_to_needy_map[best_match].append(person.user_id)

			
			for donated_item in items_donated_by_best_match:
				
				result =list(filter(lambda x : x.menu_item_id == donated_item.menu_item_id, person.needs))
				
				requested_item = result[0]
				
				requested_to_donated_item_map[requested_item] = donated_item
				
				helpers_index[best_match].donated_items.remove(donated_item)
				
				item_to_helper_map[donated_item.menu_item_id].remove(best_match)
				
				if not item_to_helper_map[donated_item.menu_item_id]:
					item_to_helper_map.pop(donated_item.menu_item_id)
				
				person.needs.remove(requested_item)

				helpful_index = update(helpful_index, requested_item.menu_item_id)
					
			
			if not item_to_helper_map:
				break

			print('')
		if not item_to_helper_map:
				break

	return requested_to_donated_item_map, needy_to_helper_map, helper_to_needy_map

class NeedyPerson:
	def __init__( self, user_id, needs):
		self.needs = needs
		self.user_id = user_id
	
	def __repr__( self ):
		return '<NeedyPerson user_id={} requested_items = {}>'.format(self.user_id, self.needs)

class Helper:
	def __init__( self, user_id, donated_items):
		self.donated_items = donated_items
		self.user_id = user_id
		
	def __repr__( self ):
		return '<Helper user_id={} donated_items = {} >'.format(self.user_id, self.donated_items)
class RequestedItem:

	def __init__(self, id, item_id):
		self.menu_item_id = item_id
		self.id = id

	def __repr__( self ):
		return '<RequestedItem id={} menu_id={}>'.format(self.id, self.menu_item_id)
class DonatedItem:
	def __init__(self, id,item_id ):
		self.menu_item_id = item_id
		self.id = id
	def __repr__( self ):
		return '<DonatedItem id={} menu_id={}>'.format(self.id, self.menu_item_id)
if __name__ == '__main__':
	
	ri1 = RequestedItem(1,4)
	ri2 = RequestedItem(2,5)
	ri3 = RequestedItem(3,4)
	ri4 = RequestedItem(4,1)
	ri5 = RequestedItem(5,5)
	ri6 = RequestedItem(6,2)
	ri7 = RequestedItem(7,3)

	di1 = DonatedItem(1,1)
	di2 = DonatedItem(2,4)
	di3 = DonatedItem(3,5)
	di4 = DonatedItem(4,4)
	di5 = DonatedItem(5,2)
	di6 = DonatedItem(6,5)
	di7 = DonatedItem(7,2)
	#needy = [ [1,24],[2,9],[3,18], [4,4]]
	#helpers = [[11,25],[12,10],[13,16],[14,2]]

	n1 = NeedyPerson(1,[ri1,ri2])
	n2 = NeedyPerson(2,[ri3,ri4])
	n3 = NeedyPerson(3,[ri5, ri6])
	n4 = NeedyPerson(4,[ri7])

	h1 = Helper(11,[di1,di2,di3])
	h2 = Helper(12,[di4,di5])
	h3 = Helper(13,[di6])
	h4 = Helper(14,[di7])

	# output = generateMapping([n1,n2,n3,n4],[h1,h2,h3,h4])
	# for k,v in output[-1].items():
	# 	print(k,v)
	

	#needy = [ [1,24],[2,9],[3,18], [4,4]]
	#helpers = [[11,16],[12,10],[13,16],[14,2],[15,8],[16,1]]	

	di1 = DonatedItem(1,5)
	di2 = DonatedItem(2,4)
	di4 = DonatedItem(4,2)
	di5 = DonatedItem(5,5)
	di6 = DonatedItem(6,2)
	di7 = DonatedItem(7,4)
	di8 = DonatedItem(8,1)
	di9 = DonatedItem(9,3)

	h1 = Helper(11,[di1])
	h2 = Helper(12,[di2,di4])
	h3 = Helper(13,[di5])
	h4 = Helper(14,[di6])
	h5 = Helper(15,[di7])
	h6 = Helper(16,[di8,di9])

	# output = generateMapping([n1,n2,n3,n4],[h1,h2,h3,h4,h5,h6])
	# for k,v in output[1].items():
	# 	print(k,v)


# needy = [ [1,24],[2,9],[3,18], [4,4]]
# helpers = [[11,23],[12,10],[13,16],[14,2],[15,26]]

	di1 = DonatedItem(1,1)
	di2 = DonatedItem(2,2)
	di3 = DonatedItem(3,3)
	di4 = DonatedItem(4,4)
	di5 = DonatedItem(5,3)
	di6 = DonatedItem(6,2)
	di7 = DonatedItem(7,5)
	di8 = DonatedItem(8,2)
	di9 = DonatedItem(9,5)
	di10 = DonatedItem(10,2)

	h1 = Helper(11,[di1, di2, di3, di4])
	h2 = Helper(12,[di5,di6])
	h3 = Helper(13,[di7])
	h4 = Helper(14,[di8])
	h5 = Helper(15,[di9, di10])

	output = generateMapping([n1,n2,n3,n4],[h1,h2,h3,h4,h5,h6])
	for k,v in output[1].items():
		print(k,v)







		
			

	





