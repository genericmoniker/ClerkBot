import labels
from reportlab.graphics import shapes

from clerk import lds_session
from clerk.paths import OUTPUT_DIR


def create_label_spec():
    """Create a label specification with 3x10 labels per sheet.

    Tested against Avery 8160 (Avery 5160 template).
    """
    # The labels library takes measurements in millimeters (1 inch = 25.4 mm).
    return labels.Specification(
        sheet_width=215.9,   # 8 1/2"
        sheet_height=279.4,  # 11"
        rows=10,
        columns=3,
        label_width=66.669,  # 2 5/8"
        label_height=25.4,   # 1"
        left_margin=4,
        column_gap=4,
        top_margin=12,
        row_gap=0,
        corner_radius=2,
    )


def draw_label(label, width, height, obj):
    """Callback function to draw a label.

    :param label: ReportLab drawing object.
    :param width: width of the label object in points.
    :param height: height of the label object in points.
    :param obj: object to draw (param to `sheet.add_label`).
    """
    # ReportLab documentation:
    # https://www.reportlab.com/docs/reportlab-userguide.pdf
    # USPS address block guidelines:
    # http://about.usps.com/publications/pub177/welcome.htm

    font = 'Helvetica'
    font_size = 10
    pad = 4

    line_height = font_size + pad
    x = pad
    y = [height - pad]  # In a list for closure modification.

    def print_line(text=''):
        y[0] -= line_height
        label.add(
            shapes.String(x, y[0], text, fontName=font, fontSize=font_size)
        )

    for line in obj:
        print_line(str(line))


def create_label(sheet, record):
    lines = []
    name = reorder_name(record['coupleName'])
    lines.append(name)
    lines.extend(record[f'desc{i}'] for i in range(1, 6) if record[f'desc{i}'])
    sheet.add_label(lines)


def reorder_name(name: str):
    """Convert 'lastname, firstname' to 'firstname lastname'."""
    parts = name.partition(', ')
    return parts[2] + ' ' + parts[0]


def create_labels(s=None):
    """Create mailing labels (PDF) for each head of house + spouse (if any)."""
    # To debug label placement, setting border=True might help.
    sheet = labels.Sheet(create_label_spec(), draw_label, border=True)

    s = s or lds_session.login()
    unit = lds_session.get_unit_number(s)
    directory = lds_session.get_directory(s, unit)
    for record in directory:
        create_label(sheet, record)

    file = OUTPUT_DIR / 'mailing_labels.pdf'
    sheet.save(str(file))
    print(
        f'{sheet.label_count} label(s) ' 
        f'on {sheet.page_count} sheet(s) ' 
        'saved to', file
    )


if __name__ == '__main__':
    create_labels()
