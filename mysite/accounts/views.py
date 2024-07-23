from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from statistics import mean
from django.http import HttpResponseRedirect
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse, JsonResponse

from .forms import CustomUserCreationForm, InscriereForm, CustomUserChangeForm
from .models import CustomUser, IncarcarePDF


# Create your views here.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class ChangeDataView():
    form_class = CustomUserChangeForm
    template_name = "registration/login.html"


def homeView(request):
    return render(request, 'home.html', {})


@login_required(login_url='/')
def inscriereView(request):
    if not request.user.rol == 'Student':
        return redirect('home')

    user = request.user
    try:
        incarcare_pdf = IncarcarePDF.objects.get(user=user)
    except IncarcarePDF.DoesNotExist:
        incarcare_pdf = None

    if request.method == "POST":
        form = InscriereForm(request.POST, request.FILES)
        if form.is_valid():
            if incarcare_pdf:
                incarcare_pdf.titlul_lucrarii = form.cleaned_data['titlul_lucrarii']
                incarcare_pdf.descrierea_lucrarii = form.cleaned_data['descrierea_lucrarii']
                incarcare_pdf.eseu = form.cleaned_data['eseu']
                incarcare_pdf.fisa_inscriere = form.cleaned_data['fisa_inscriere']
                incarcare_pdf.declaratie_autenticitate = form.cleaned_data['declaratie_autenticitate']
            else:
                incarcare_pdf = IncarcarePDF(
                    user=user,
                    titlul_lucrarii=form.cleaned_data['titlul_lucrarii'],
                    descrierea_lucrarii=form.cleaned_data['descrierea_lucrarii'],
                    eseu=form.cleaned_data['eseu'],
                    fisa_inscriere=form.cleaned_data['fisa_inscriere'],
                    declaratie_autenticitate=form.cleaned_data['declaratie_autenticitate']
                )
            incarcare_pdf.save()

            user.este_inscris = True
            user.status = 'waiting'
            user.rejection_reason = ''
            user.save()
            messages.success(request, "Ai incărcat cu succes documentele")
            return redirect('home')
    else:
        form = InscriereForm()

    context = {
        'form': form,
        'status': user.status,
        'este_inscris': user.este_inscris,
        'rejection_reason': user.rejection_reason,
    }

    return render(request, "upload.html", context)


@login_required()
def verify_uploads(request):
    if not request.user.rol == "Secretar":
        return redirect('home')

    users = CustomUser.objects.filter(rol='Student', este_inscris=True).exclude(status='approved')

    if request.method == 'POST':
        for user in users:
            status = request.POST.get(f'status_{user.id}')
            rejection_reason = request.POST.get(f'rejection_reason_{user.id}', '')

            print(f"User: {user.username}, Status: {status}, Rejection Reason: {rejection_reason}")

            try:
                incarcare_pdf = IncarcarePDF.objects.get(user=user)
            except IncarcarePDF.DoesNotExist:
                incarcare_pdf = None

            if status:
                if status == 'approved':
                    user.status = 'approved'
                    user.rejection_reason = ''
                elif status == 'rejected':
                    user.status = 'rejected'
                    user.rejection_reason = rejection_reason
                    user.este_inscris = False
                    try:
                        incarcare_pdf = IncarcarePDF.objects.get(user=user)
                        incarcare_pdf.eseu.delete()
                        incarcare_pdf.fisa_inscriere.delete()
                        incarcare_pdf.declaratie_autenticitate.delete()
                        incarcare_pdf.delete()
                    except IncarcarePDF.DoesNotExist:
                        pass
                else:
                    user.status = 'waiting'
                    user.rejection_reason = ''

                user.save()

        return redirect('verify_uploads')

    user_incarcare_pairs = [(user, IncarcarePDF.objects.get(user=user)) for user in users if
                            IncarcarePDF.objects.filter(user=user).exists()]

    return render(request, 'verify_uploads.html', {'user_incarcare_pairs': user_incarcare_pairs})


@login_required
def list_students(request):
    if request.user.rol == 'Membru comisie':
        students = CustomUser.objects.filter(rol='Student', status='approved')
        return render(request, 'list.html', {'students': students})
    else:
        return redirect('home')


@login_required
def grade_student(request, student_id):
    if request.user.rol == 'Membru comisie':
        student = get_object_or_404(CustomUser, id=student_id)

        if request.method == 'POST':
            nota1 = float(request.POST.get('nota1'))
            nota2 = float(request.POST.get('nota2'))

            # Verifică dacă notele sunt în intervalul corect
            if 1 <= nota1 <= 10 and 1 <= nota2 <= 10:
                # Adaugă notele la student
                student.nota1.append(nota1)
                student.nota2.append(nota2)

                # Calculează nota finală
                if student.nota1 and student.nota2:
                    student.notaFinala = round((mean(student.nota1) + mean(student.nota2)) / 2, 2)
                else:
                    student.notaFinala = None

                student.save()

                return redirect('list_students')

        return render(request, 'grade_student.html', {'student': student})
    else:
        return redirect('home')


@login_required
def final_grades(request):
    if request.user.rol == 'Secretar':
        students = CustomUser.objects.filter(rol='Student')
        student = CustomUser(request.user)
        if request.user.is_role == "Student":
            student.notaFinala = round((mean(student.nota1) + mean(student.nota2)) / 2, 2)
        return render(request, 'final_grades.html', {'students': students})
    else:
        return redirect('home')


@login_required
def toggle_afisare_note(request):
    if request.user.rol == 'Secretar':
        afisare_note = CustomUser.objects.filter(rol='Student').values_list('afisare_note', flat=True).first()
        new_state = not afisare_note
        toggle_message = "Acum studentii pot vedea notele!" if new_state else "Acum studentii nu pot vedea notele!"
        students = CustomUser.objects.filter(rol='Student')
        student = CustomUser(request.user)
        if request.user.is_role == "Student":
            student.notaFinala = round((mean(student.nota1) + mean(student.nota2)) / 2, 2)
        CustomUser.objects.filter(rol='Student').update(afisare_note=new_state)
        toggle_message = "Acum studentii pot vedea notele!" if new_state else "Acum studentii nu pot vedea notele!"
        return render(request, 'final_grades.html', {'students': students, 'toggle_message': toggle_message})
    else:
        return redirect('home')


def generate_pdf(request):
    if request.user.rol == 'Student':
        # Obținem utilizatorul curent autentificat
        user = request.user

        # Filtrăm studentul curent pentru a-i genera fișierul PDF
        student = CustomUser.objects.get(id=user.id)

        # Setăm răspunsul HTTP pentru descărcare
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Rezultate.Licenta.2024.pdf"'

        # Generăm PDF-ul utilizând reportlab
        pdf = canvas.Canvas(response, pagesize=letter)
        pdf.setTitle("Notele tale")

        pdf.drawString(200, 770, "Notele obtinute la examenul de licenta 2024:")
        pdf.drawString(100, 700, "Nume:")
        pdf.drawString(100, 650, "Initiala tatalui:")
        pdf.drawString(100, 600, "Prenume:")
        pdf.drawString(100, 550, "Titlul lucrarii:")
        pdf.drawString(100, 500, "Nota 1 acordata de membrii comisiei:")
        pdf.drawString(100, 450, "Nota 2 acordata de membrii comisiei:")
        pdf.drawString(100, 400, "Nota finala:")

        x = 350
        pdf.drawString(x, 700, student.nume)
        pdf.drawString(x, 650, student.initiala_tatalui)
        pdf.drawString(x, 600, student.prenume)
        pdf.drawString(x, 550, student.incarcarepdf.titlul_lucrarii)
        pdf.drawString(x, 500, ', '.join(map(str, student.nota1)))
        pdf.drawString(x, 450, ', '.join(map(str, student.nota2)))
        pdf.drawString(x, 400, str(student.notaFinala))

        pdf.showPage()
        pdf.save()

        return response
    else:
        return HttpResponse("Unauthorized", status=401)

@login_required
def view_grades(request):
    if request.user.rol == 'Student' and CustomUser.objects.filter(rol='Student').values_list('afisare_note', flat=True).first():
        students = CustomUser.objects.filter(rol='Student')
        student = CustomUser(request.user)
        if request.user.is_role == "Student":
            student.notaFinala = round((mean(student.nota1) + mean(student.nota2)) / 2, 2)
        return render(request, 'student_grades.html', {'students': students})
    else:
        return redirect('home')