from flask_wtf import FlaskForm
from wtforms.fields import SelectField, BooleanField, IntegerField
from wtforms.validators import ValidationError
from wtforms.widgets import HTMLString, html_params
from cgi import escape
from wtforms.widgets import Select
from app import db
from sqlalchemy import func
from models import Apartment

# very loosely based on https://gist.github.com/playpauseandstop/1590178

__all__ = ('ExtendedSelectField', 'ExtendedSelectWidget')


class ExtendedSelectWidget(Select):
    """
    Add support of choices with ``optgroup`` to the ``Select`` widget.
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if self.multiple:
            kwargs['multiple'] = True
        html = ['<select %s>' % html_params(name=field.name, **kwargs)]
        for item1, item2 in field.choices:
            if isinstance(item2, (list,tuple)):
                group_label = item1
                group_items = item2
                html.append('<optgroup %s>' % html_params(label=group_label))
                for inner_val, inner_label in group_items:
                    html.append(self.render_option(inner_val, inner_label, inner_val == field.data))
                html.append('</optgroup>')
            else:
                val = item1
                label = item2
                html.append(self.render_option(val, label, val == field.data))
        html.append('</select>')
        return HTMLString(''.join(html))


class ExtendedSelectField(SelectField):
    """
    Add support of ``optgroup`` grouping to default WTForms' ``SelectField`` class.

    Here is an example of how the data is laid out.

        (
            ('Череповецкий район','Череповецкий район'),
            ('Шекснинский район','Шекснинский район'),
            ('Вологодский район','Вологодский район'),
            ('Б', (
                ('Бабаевский район', 'Бабаево'),
                ('Бабушкинский район', 'Село имени Бабушкина'),
                ('Белозерский район', 'Белозерск')
            )),
            ('Vegetables', (
                ('cucumber', 'Cucumber'),
                ('potato', 'Potato'),
                ('tomato', 'Tomato'),
            ))

        )

    It's a little strange that the tuples are (value, label) except for groups which are (Group Label, list of tuples)
    but this is actually how Django does it too https://docs.djangoproject.com/en/dev/ref/models/fields/#choices

    """
    widget = ExtendedSelectWidget()

    def pre_validate(self, form):
        """
        Don't forget to validate also values from embedded lists.
        """
        for item1,item2 in self.choices:
            if isinstance(item2, (list, tuple)):
                group_label = item1
                group_items = item2
                for val,label in group_items:
                    if val == self.data:
                        return
            else:
                val = item1
                label = item2
                if val == self.data:
                    return
        raise ValueError(self.gettext('Not a valid choice!'))




class PastebinEntry(FlaskForm):
    language = ExtendedSelectField(u'Programming Language', choices=(
            ('Череповецкий район','Череповец'),
            ('Шекснинский район','Шексна'),
            ('Вологодский район','Вологда'),
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

        ), default=('Череповецкий район','Череповец'))
    new_building = BooleanField('Новостройка', default=True)
    min_cost = IntegerField('Минимальная цена', default=db.session.query(func.min(Apartment.price)).scalar())
    max_cost = IntegerField('Максимальная цена', default=db.session.query(func.max(Apartment.price)).scalar())
