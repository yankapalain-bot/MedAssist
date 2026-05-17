from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q

# ------------------------------------------------------------------------------
# HTMX template mixin
# ------------------------------------------------------------------------------

class HtmxTemplateMixin:
    """
    Switches the template to a partial when the request comes from HTMX.

    When a user types in the search box, HTMX sends a GET request with
    the header HX-Request: true. This mixin detects that header and
    renders only the rows partial (e.g. patient_rows.html) instead of
    the full page.

    This is what makes the search feel instant: only the table rows are
    replaced, not the whole page.
    """
    partial_template_name = None
    
    def is_htmx(self):
        return self.request.headers.get("HX-Request") == "true"

    def get_template_names(self):
        if self.is_htmx() and self.partial_template_name:
            return [self.partial_template_name]
        return super().get_template_names()
       


# ------------------------------------------------------------------------------
# Staff-required mixin
# ------------------------------------------------------------------------------

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser
    

# ------------------------------------------------------------------------------
# Searchable list mixin
# ------------------------------------------------------------------------------

class SearchableListMixin:
    
    search_fields = ()

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q and self.search_fields:
            query = Q()
            for field in self.search_fields:
                query |= Q(**{f"{field}__icontains": q})                
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        
        return context


