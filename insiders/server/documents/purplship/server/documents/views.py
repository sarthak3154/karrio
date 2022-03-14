from django.urls import re_path
from django.core.files.base import ContentFile
from django_downloadview import VirtualDownloadView

from purplship.server.documents import models
from purplship.server.documents.generator import Documents


class DocumentGenerator(VirtualDownloadView):
    def get(
        self,
        request,
        pk: str,
        slug: str,
        **kwargs,
    ):
        """Generate a document."""
        template = models.DocumentTemplate.objects.get(pk=pk, slug=slug)
        query_params = request.GET.dict()

        self.document = Documents.generate(template, query_params, context=request)
        self.name = f"{slug}.pdf"
        self.attachment = query_params.get("download", False)

        response = super(DocumentGenerator, self).get(request, pk, slug, **kwargs)
        response["X-Frame-Options"] = "ALLOWALL"
        return response

    def get_file(self):
        return ContentFile(self.document.getvalue(), name=self.name)


urlpatterns = [
    re_path(
        r"^documents/(?P<pk>\w+).(?P<slug>\w+)",
        DocumentGenerator.as_view(),
        name="documents-generator",
    )
]
