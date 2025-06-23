from django import forms
from .models import Task

class NewTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = False
        self.fields['description'].label = False
        self.fields['deadline'].label = False

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline']

        widgets = {
            'title': forms.TextInput(
                attrs={ 'label': 'Add a task..',
                    'class': 'form-control rounded-md p-1 font-light text-[#9abad8] bg-[#0d1c2a] outline-none w-[93%] md:w-full',
                    'placeholder': 'Add a task..',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control rounded-md p-1 font-light text-[#9abad8] bg-[#0d1c2a] outline-none w-[93%] md:w-full mt-3',
                    'placeholder': 'Add a description..',
                    'rows': 2,
                }
            ),
            'deadline': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control rounded-md p-1 font-light text-[#9abad8] bg-[#0d1c2a] outline-none w-[93%] md:w-full',
                }
            ),
        }
