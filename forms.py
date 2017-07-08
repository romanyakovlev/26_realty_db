from flask_wtf import FlaskForm
from wtforms.fields import SelectField, BooleanField, IntegerField
from wtforms.widgets import HTMLString, html_params
from wtforms.widgets import Select
from main import db
from sqlalchemy import func
from models import Apartment


class ExtendedSelectWidget(Select):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = ['<select {}>'.format(html_params(name=field.name, **kwargs))]
        for item1, item2 in field.choices:
            if isinstance(item2, (list, tuple)):
                group_label, group_items = item1, item2
                html.append('<optgroup {}>'.format(html_params(label=group_label)))
                for inner_val, inner_label in group_items:
                    html.append(self.render_option(inner_val, inner_label, inner_val is field.data))
                html.append('</optgroup>')
            else:
                val, label = item1, item2
                html.append(self.render_option(val, label, val == field.data))
        html.append('</select>')
        return HTMLString(''.join(html))


class ExtendedSelectField(SelectField):

    widget = ExtendedSelectWidget()

    def pre_validate(self, form):
        for item1, item2 in self.choices:
            if isinstance(item2, (list, tuple)):
                group_label, group_items = item1, item2
                for val, label in group_items:
                    if val is self.data:
                        break
            else:
                val, label = item1, item2
                if val is self.data:
                    break
        raise ValueError(self.gettext('Not a valid choice'))


class ApartmentListForm(FlaskForm):
    oblast_district = ExtendedSelectField('Город', choices=(
            ('Череповецкий район', 'Череповец'),
            ('Шекснинский район', 'Шексна'),
            ('Вологодский район', 'Вологда'),
            ('Б', (
                ('Бабаевский район', 'Бабаево'),
                ('Бабушкинский район', 'Село имени Бабушкина'),
                ('Белозерский район', 'Белозерск')
            )),
            ('В', (
                ('Великоустюгский район', 'Великий устюг'),
                ('Верховажский район', 'Верховажье'),
                ('Вожегодский район', 'Вожега'),
                ('Вологодский район', 'Вологда'),
            )),
            ('Г', (
                ('Грязовецкий район', 'Грязовец'),
            )),
            ('К', (
                ('Кадуйский район', 'Кадуй'),
                ('Кирилловский район', 'Кириллов'),
                ('Кичменгско-Городецкий район', 'Кичменгский Городок'),
            )),
            ('Л', (
                ('Вашкинский район', 'Липин Бор'),
            )),
            ('Н', (
                ('Никольский район', 'Никольск'),
                ('Нюксенский район', 'Нюксеница'),
            )),
            ('С', (
                ('Сокольский район', 'Сокол'),
                ('Сямженский район', 'Сямжа'),
            )),
            ('Т', (
                ('Тарногский район', 'Тарногский Городок'),
                ('Тотемский район', 'Тотьма'),
            )),
            ('У', (
                ('Усть-Кубинский район', 'Устье'),
                ('Устюженский район', 'Устюжна'),
            )),
            ('Х', (
                ('Харовский район', 'Харовск'),
            )),
            ('Ч', (
                ('Чагодощенский район', 'Чагода'),
                ('Череповецкий район', 'Череповец'),
            )),
            ('Ш', (
                ('Шекснинский район', 'Шексна'),
                ('Междуреченский район', 'Шуйское'),
            )),

    ), default=('Череповецкий район', 'Череповец'))
    new_building = BooleanField('Новостройка', default=False)
    min_cost = IntegerField('Минимальная цена',
                            default = db.session.query(func.min(Apartment.price)).scalar())
    max_cost = IntegerField('Максимальная цена',
                            default=db.session.query(func.max(Apartment.price)).scalar())
