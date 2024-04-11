from .models import Manseryuk
from django.views.generic import CreateView, DetailView
from django.urls import reverse
from .forms import ManseryukForm
from manseryuk.views import Msr_Calculator
from .utils import determine_zodiac_hour_str
class msrInputView(CreateView):
    model = Manseryuk
    form_class = ManseryukForm
    template_name = "mrdg/msr_input.html"

    def get_success_url(self):
        return reverse("msr-detail", kwargs={"msr_id": self.object.id})


class msrDetailView(DetailView):
    model = Manseryuk
    template_name = "mrdg/msr_detail.html"
    pk_url_kwarg = "msr_id"
    context_object_name = 'msr'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        this_msr = Manseryuk.objects.get(pk=self.kwargs.get('msr_id'))
        
        data = Msr_Calculator()
        time = determine_zodiac_hour_str(this_msr.hour, this_msr.min)
        datas = data.getAll(this_msr.year, this_msr.month, this_msr.day,
                            time, this_msr.sl, this_msr.gen, this_msr.yd)
        context["datas"] = datas
        return context
