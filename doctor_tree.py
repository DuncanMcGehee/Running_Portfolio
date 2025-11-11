class DoctorNode:
    def __init__(self, name):
        self.name = name 
        self.left = None 
        self.right = None
    pass # Delete this line and implement the DoctorNode class



class DoctorTree:
    def __init__(self):
        self.root = None
    
    def insert(self, supervisor_name, doctor_name, side, current_node=None):
        if self.root is None: 
            print("The tree is empty. Setting employee as root.")
            return
        if current_node is None:  
            current_node = self.root
        if current_node.name == supervisor_name:
            if side == "left" and current_node.left is None:
                current_node.left = DoctorNode(doctor_name) 
                print(f"Inserted {doctor_name} to the left of {supervisor_name}") 
            elif side == "right" and current_node.right is None: 
                current_node.right = DoctorNode(doctor_name)  
                print(f"Inserted {doctor_name} to the right of {supervisor_name}")
            else: 
                print("The side inputted is already occupied.")
                return
        elif current_node.left is not None and current_node.right is not None: 
            self.insert(supervisor_name, doctor_name, side, current_node.left) 
            self.insert(supervisor_name, doctor_name, side, current_node.right) 
        

    def preorder(self, current_node=None):
        if current_node is None:
            return []
        result = [current_node.name] 
        result += self.preorder(current_node.left) 
        result += self.preorder(current_node.right) 
        return result
            
    def inorder(self, current_node=None):
        if current_node is None:
            return []
        result = self.inorder(current_node.left) 
        result.append(current_node.name) 
        result += self.inorder(current_node.right) 
        return result

    def postorder(self, current_node=None):
        if current_node is None:
            return []
        result = self.postorder(current_node.left) 
        result += self.postorder(current_node.right) 
        result.append(current_node.name) 
        return result


# Test your DoctorTree and DoctorNode classes here
tree = DoctorTree()
tree.root = DoctorNode("Dr. Croft") 
# Insert values
tree.insert("Dr. Croft", "Dr. Goldsmith", "right") 
tree.insert("Dr. Croft", "Dr. Phan", "left")
tree.insert("Dr. Phan", "Dr. Carson", "right") 
tree.insert("Dr. Phan", "Dr. Morgan", "left")
print(tree.preorder(tree.root)) # ["Dr. Croft", "Dr. Phan", "Dr. Morgan", "Dr. Carson", "Dr. Goldsmith"]
print(tree.inorder(tree.root)) # ["Dr. Morgan", "Dr. Phan", "Dr. Carson", "Dr. Croft", "Dr. Goldsmith"]
print(tree.postorder(tree.root)) # ["Dr. Morgan", "Dr. Carson", "Dr. Phan", "Dr. Goldsmith", "Dr. Croft"] 


'''
Why is a tree appropriate for the doctor structure? 
A tree is perfect for the doctor structure because you want to be able to list the doctors in a specific order 
by name. The order that you want them listed can also be manipulated by the process you choose. This is why we 
can make preorder, inorder, and postorder to change the direction of the tree that we are traversing.

When might a software engineer use preorder, inorder, or postorder traversals?
Preorder should be used when you think the root is the most important or every child is centralized by their parent.
This allows for a drilling down logic system. Inorder is used when you want to travel left to right, this could be 
useful when the tree is sorted in a specific manner or you need to preform mathmatical expressions. Postorder is perfect
for when you need the children to be processed before their parent is ever touched.

How do heaps help simulate real-time systems like emergency intake?
Heaps simulate real-time systems like emergency intake by allowing the system to have a way to sort itself by urgency.
Lists are great but it's difficult and costly to make them sort themselves. With heaps we can make allow the tree to sort 
itself due to the urgency of the patients problem, which having priority for an urgent care system is crucially important 
because different problems are far from equal.

'''