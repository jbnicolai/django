# -*- coding:utf8 -*-

from django.template import Context, loader, Template
from django.conf import settings
from urllib import unquote
import django, sys, json

class Session(object):
    """Render Session"""
    def __init__(self, template_dirs = '.'):
        super(Session, self).__init__()
        self.template_dirs = template_dirs
        settings.configure(DEBUG = True, TEMPLATE_DEBUG = True, TEMPLATE_DIRS = [template_dirs], LANGUAGE_CODE = 'zh-cn', FILE_CHARSET = 'utf-8', TIME_ZONE = 'Asia/Shanghai')
        django.setup()
    def renderFile(self, tpl, data = {}):
        """Render a template with mock data"""
        template = loader.get_template(tpl)
        context = Context(data)
        return template.render(context)
    def render(self, source, data = {}):
        """Render from source"""
        template = Template(source)
        context = Context(data)
        return template.render(context)
    def __str__(self):
        print 'template_dirs:' + self.template_dirs

if __name__ == '__main__':
    if len(sys.argv) < 3:
        #arguments.length < 3
        #python index.py < source < mock
        source = unquote(sys.stdin.readline())
        mockStr = sys.stdin.readline()
        session = Session()
        try:
            data = json.loads(mockStr)
        except Exception,e:
            #ignore broken mock string format
            data = {}
        html = session.render(source ,data).encode('utf-8')
    else:
        #arguments.length >= 3
        #python index.py dirs tpl < mock
        dirs = unquote(sys.argv[1])#template_dirs is a directory path that is quoted
        session = Session(dirs)

        tpl = unquote(sys.argv[2])#template is a file path that is quoted

        mockStr = sys.stdin.readline()#We read the mock data from stdin

        try:
            data = json.loads(mockStr)
        except Exception,e:
            #ignore broken mock string format
            data = {}

        html = session.renderFile(tpl, data).encode('utf-8')
    sys.stdout.write(html)
    sys.stdout.flush()
    sys.exit()
