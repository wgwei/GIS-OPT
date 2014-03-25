# help files
def help_dbf_shape():
    """ shape file include *.shp, *.shx and *.dbf,
        where *.shp contains the
        type of shape:
        shpTypes = {'Point':       shapelib.SHPT_POINT,
                'PointList':   shapelib.SHPT_MULTIPOINT,
                'LineSegment': shapelib.SHPT_ARC,
                'Line':        shapelib.SHPT_ARC,
                'LineList':    shapelib.SHPT_ARC,
                'Polygon':     shapelib.SHPT_POLYGON}
                SHPT_ARC = 3
                SHPT_MULTIPOINT = 8
                SHPT_NULL = 0
                SHPT_POINT = 1
                SHPT_POLYGON = 5    more information use help(shapelib)
        the ID of shapes,    
        and the vertices of the shapes in list: [[(x, y, ...), ...], ...].        

        The main classes are SHPObject and ShapeFile.
            shp = ShapeFile(filename) will return a shape class shp.

        # data structure
            (type, ID, vertix=[[(x,y,...),...]]). This is called one object of the shape
            file.

        # aquire basic information
            shp.info() -> (num_shapes, type, (x_min, y_min, z_min, m_min),
                      (x_max, y_max, z_max, m_max)) to get the basic information of
                      a shape file.

        # read object
            shpObj = shp.read_object(objID) as shpObj.
        We can use:
            shpObj.extents() -> ((x_min, y_min, z_min, m_min),
                                (x_max, y_max, z_max, m_max))
            shpObj.part_types() -> a tuple of integers, each integer indicating
                                    the type of the corresponding part in vertice
            shpObj.vertices() -> [[(x, y, ...), ...], ...]. Returns a list of object
                                parts, where each part is again a list of vertices.
                                Each vertex is a tuple of two to four doubles,
                                depending on the object test_shape.shx

        # write object/shape file out                    
            The structure of one object is (type, ID, vertix=[[(x,y,...),...]])
            Then we can use:
            w2shp = shapelib.create(file, type)
            w2shp.write_object(id, shpObj) to write an object to a shape file or we can
            use shpObj = shapelib.SHPObject(type, ID, vertix=[[(x,y,...),...]]) to create
            and object first and then use w2shp.write_object(id, shpObj) to write this
            object to a shape file.
        
            After all, use shp.close() and w2shp.close() to close the shape file.
        

        ############################################################
        However, the shape file only contains the shape information, if we want to
        add more information to attached to the shape file, then we need *.dbf file

        # *.dbf data structure:
        The structure of dbf data is a table of data. the first row is called field.
        The other rows are called the records. Each value in the table is called
        attribute.
        
        # The type of fields are:
        fieldType = {"integer": dbflib.FTInteger,
                     "double":   dbflib.FTDouble, 
                     "string":   dbflib.FTstring,
                     "logical":  dbflib.FTLogical,
                     "invalid":  dbflib.FTInvalid}
                     where,
                     FTString = 0,
                     FTInteger = 1,
                     FTDouble = 2,
                     FTLogical = 3,
                     FTInvalid = 4 more information use help(dbflib)
                    
        # aquier basic information:
            dbf = dbflib.open(dbfFile) to open a dbf file
            field_info(field_index) -> (type, name, width, decimals)
            dbf.field_count() -> integer. to count the number of field
            dbf.record_count() -> integer. to count the number of record.

        # read attribute or record:
            record = dbf.read_record(ID) to read a record in dictionary: 
                {field1: attribute1, "field2": attribute2,...}. then we can
                query the attribute by record[field1], record["field2"], ...
                                                    
            dbf.read_attribute(recordID, fieldID) returan the attribute value.

        # write records or attributes to an .dbf file 
          1. create dbf file
            dbf = dbflib.create('filename.dbf')
          2. add field to the .dbf file
              dbf.add_field(fieldname, type, width, decimal) # type is an integer.
        
          3.  write attribute or record:
            dbf.write_attribute(record_index, field_index, new_value) # write new attribute
            dbf.write_record(record_index, record) -> record_index # to write a new record
                Record can either be a dictionary in which case the keys are used as
                field names, or a sequence that must have an item for every field
                (length = field_count())
          4. dbf.close()
          
          EXAMPLE OF ATTACH FIELD TO GENERATE A NEW PDF FILE
            def attachField(originFileName, attachedFileName, aimFileName):
                orf = dbflib.open(originFileName)
                atf = dbflib.open(attachedFileName)
                amf = dbflib.create(aimFileName)
                assert (orf.record_count()==atf.record_count())
                # add filed of original files
                oNum = orf.field_count()
                aNum = atf.field_count()
                for f in range(oNum):
                    fi = orf.field_info(f)
                    amf.add_field(fi[1], fi[0], fi[2], fi[3])
                # add field of attached files
                for f in range(aNum):
                    fi = atf.field_info(f)
                    amf.add_field(fi[1], fi[0], fi[2], fi[3])
                for r in range(orf.record_count()):
                    # write in original file
                    for n in range(oNum):
                        amf.write_attribute(r, n, orf.read_attribute(r, n))
                    for m in range(aNum):
                        amf.write_attribute(r, oNum+m, atf.read_attribute(r, m))
                orf.close()
                atf.close()
                amf.close()
        
            EXAMPLE OF MIX SHAPE FILES AND DBF FILES
            import shapelib
            import dbflib
            class MixZones():
                def __init__(self, newFile):
                    self.zoneNum = [1, 2,3 ,4, 5, 6, 7, 8,9, 10, 11]
                    self.nSHP = shapelib.create(newFile, shapelib.SHPT_POINT)
                    self.nDBF = dbflib.create(newFile)
                    
                def _mixZones(self):
                    cnt = 0
                    for n in self.zoneNum:
                        zoneShpFile = 'receiver_zone_'+str(n)
                        print 'Operating ', zoneShpFile
                        SHP = shapelib.open(zoneShpFile)
                        DBF = dbflib.open(zoneShpFile)
                        if n==1:
                            for f in xrange(DBF.field_count()):
                                fi = DBF.field_info(f)
                                self.nDBF.add_field(fi[1], fi[0], fi[2], fi[3])
                        for s in xrange(SHP.info()[0]):
                            shpObj = SHP.read_object(s)
                            dbfRec = DBF.read_record(s)
                            self.nSHP.write_object(cnt, shpObj)
                            self.nDBF.write_record(cnt, dbfRec)
                            cnt += 1
                        SHP.close()
                        DBF.close()
                    self.nDBF.close()
                    self.nSHP.close()
            
            if __name__=='__main__':
                obj = MixZones('allZones')
                obj._mixZones()
    """

if __name__=="__main__":
    help (help_dbf_shape)
    



    
        
                
