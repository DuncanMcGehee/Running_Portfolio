class Patient:
    def __init__(self, name, urgency):
        self.name = name
        self.urgency = urgency



class MinHeap:
    def __init__(self): 
        self.data = []

    def heapify_up(self, index): 
        while index > 0: 
            parent_index = (index - 1) // 2  
            current_task = self.data[index] 
            parent_task = self.data[parent_index] 
            if current_task.urgency < parent_task.urgency:  
                temp = self.data[index] 
                self.data[index] = self.data[parent_index] 
                self.data[parent_index] = temp

                index = parent_index 
            else:
                break

    def heapify_down(self, index):
        left = 2 * index + 1 
        right = 2 * index + 2 
        smallest = index 
         
        if left < len(self.data) and self.data[left].urgency < self.data[smallest].urgency:
            smallest = left
        
        if right < len(self.data) and self.data[right].urgency < self.data[smallest].urgency:
            smallest = right
        
        if smallest != index: 
            temp = self.data[index] 
            self.data[index] = self.data[smallest] 
            self.data[smallest] = temp

            self.heapify_down(smallest)

    def insert(self, patient):
        self.data.append(patient)
        self.heapify_up(len(self.data) - 1) 

    def print_heap(self):
        for patient in self.data:
            print(f"Patient Name: {patient.name}, Urgency: {patient.urgency}")

    def peek(self):
        if not self.data:
            return None
        return self.data[0] 
    
    def remove_min(self):
        if not self.data:
            return None
        
        if len(self.data) == 1:
            return self.data.pop()
        
        min_patient = self.data[0] 
        self.data[0] = self.data.pop() 
        self.heapify_down(0) 
        return min_patient




# Test your MinHeap class here including edge cases
heap = MinHeap()
heap.insert(Patient("Jordan", 3))
heap.insert(Patient("Taylor", 1))
heap.insert(Patient("Avery", 5))
heap.print_heap()

next_up = heap.peek()
print(next_up.name, next_up.urgency) # Taylor, 1 

served = heap.remove_min()
print(served.name) # Taylor
heap.print_heap()